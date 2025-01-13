import copy
import pdb
from collections import defaultdict
from semperpy.core.tools import to_list, is_list
from semperpy.geo.domain import Domain
from gmaopy.retrieve.retriever import Retriever
from gmaopy.ods.ods import ODS
from gmaopy.ods.odsgroup import ODSGroup
from gmaopy.ods.odscleaner import ODSCleaner
#pdb.set_trace()
class ODSEngine(object):

    def newentry(self):
        d = {}
        d['obs'] = []
        d['level'] = defaultdict(set)
        d['domains'] = set()
        d['usage'] = set()
        return d

    def __init__(self,observations,actor,staging_rate = 'hour',masking = None,ignore_missing_files = False):
        self.ignore_missing_files_ = ignore_missing_files
        retriever = Retriever('semperpy',staging_rate,observations)
        self.process(retriever,actor,masking)

    def process(self,retriever,actor,masking):
        domaindef = Domain.domains('semperpy')
        #----------- loop over each run -----------------------
        for date, files in retriever.files():
            all_kt = set()
            all_types = set()
            #----------- loop over each ods file -----------------------
            for file in files:
                info = self.newentry()
                info['date'] = date
                #----------- first gather info types, levels, usage, domains  etc.. ------
                for obs in files[file]['directive']:
                    variables = actor.variables(obs)
                    all_types.add(obs['type'])
                    info['obs'].append(obs)
                    for domain in to_list(obs['domain_name']):
                        info['domains'].add(domain)
                    levels = tuple(to_list(obs['level']))
                    info['level'][obs['levtype']].add(levels)
                    info['usage'].add(obs['usage'])
                    kt = obs['kt']
                    if is_list(kt) and len(kt) == 1:
                        kt = kt[0]
                    all_kt.add(kt)
                if len(all_types) > 1:
                    raise RuntimeError('The software is not designed to mix different types of observation in the same computation, found: %s' % ', '.join(list(all_types)))
                cleaner = ODSCleaner(list(all_types)[0])
                #----------- open the ods file or group of files -----------------------
                ods = self.openODS(file,masking)
                if ods is not None:
                    #----------- compute all necessary filters for that file -----------
                    domain_filters = self.createDomainFilters(info['domains'],domaindef,ods) # code is failing here
                    level_filters = self.createLevelFilters(info['level'],ods)
                    qcexcl_variable = cleaner(ods,list(all_kt))
                    usage_filters = self.createUsageFilters(info['usage'],ods,qcexcl_variable)
                    for obs in info['obs']:
                        filter = ods.compile(self.createExpression(obs),False,qcexcl=qcexcl_variable)
                        levelFilter = self.levelFilter(obs,level_filters)
                        actor.processData(self,date,ods,obs,filter,levelFilter,domain_filters,usage_filters)
                        #print('ODS Engine Test', actor)
                    ods.close()

    def openODS(self,files,masking):
        print(files)
        ods = None
        try:
            if len(files) > 1:
                ods = ODSGroup(files,masking=masking)
            else:
                ods = ODS(files[0],masking=masking)
        except IOError as e:
            if self.ignore_missing_files_:
                print("file not found",e)
                print(files[0])
            else:
                raise
        return ods

    def createDomainFilters(self,all,domaindef,ods):
        domains = {}
        for domain in all:
            rec = {}
            d = domaindef[domain]
            rec['south'],rec['west'],rec['north'],rec['east'] = d.coordinates_sn()
            if domain != 'global':
                expr = '(lat >= %f) & (lat <= %f) & (lon >= %f) & (lon <= %f)' % (d.south_,d.north_,d.west_,d.east_)
                rec['filter'] = ods.compile(expr,False) # code is failing here
            else:
                rec['filter'] = None
            rec['domain_name'] = domain
            domains[domain] = rec
        return domains

    def createLevelFilters(self,all,ods):
        levelFilters = {}
        for levtype,levels in all.items():
            for level in levels:
                levelFilter = None
                if levtype == 'pl':
                    levelFilter = ods.sampleLevels(bins=level)
                elif levtype == 'ch':
                    levelFilter = ods.read('lev')
                elif levtype == 'depth':
                    levelFilter = ods.sampleLinearLevels(bins=level)
                elif levtype == 'wl':
                    levelFilter = ods.sampleLinearLevels(bins=level)
                elif levtype != 'sfc':
                    raise RuntimeError('unhandled level type: %s' % levtype)
                levelFilters[level] = levelFilter
        return levelFilters

    def createUsageFilters(self,all,ods,qcexcl_variable):
        usageFilters = {} 
        for usage in all:
            if usage == 'used':
                usageFilters[usage] = ods.compile('qcexcl == 0',False,qcexcl=qcexcl_variable)
            elif usage == 'passive':
                usageFilters[usage] = ods.compile('(qcexcl == 1) | (qcexcl == 7)',False,qcexcl=qcexcl_variable)
            elif usage == 'unused':
                all_unused = set(qcexcl_variable.values())
                all_unused.discard(0)
                all_unused.discard(1)
                all_unused.discard(7)
                filters = [ '(qcexcl == %d)' % x for x in all_unused ]
                if len(all_unused) > 0:
                    usageFilters['unused'] = ods.compile('| '.join(filters),False,qcexcl=qcexcl_variable)
                else:
                    usageFilters['unused'] = ods.compile('(qcexcl != qcexcl)',False,qcexcl=qcexcl_variable)
                for one in all_unused:
                    usageFilters[str(one)] = ods.compile('(qcexcl == %d)' % one,False,qcexcl=qcexcl_variable)
                usageFilters['unused_list'] = [ str(x) for x in all_unused ]
            elif usage == 'all':
                usageFilters[usage] = None
            else:
                try:
                    u = int(usage)
                    usageFilters[usage] = ods.compile('(qcexcl == %d)' % u,False,qcexcl=qcexcl_variable)
                except ValueError:
                    raise RuntimeError('Unknow usage %s' % usage)
        return usageFilters

    def createExpression(self,obs):
        terms = []
        for var in ['kx','kt']:
            terms.append('(%s == %d)' % (var,obs[var]))
        return ' & '.join(terms)

    def levelFilter(self,obs,level_filters):
        levelFilter = None
        if obs['levtype'] != 'sfc':
            levels = tuple(to_list(obs['level']))
            levelFilter = level_filters[levels]
        return levelFilter

    def extractVariable(self,variable,ods,domain,domain_filters,usage,usageFilters,filter):
        if domain_filters[domain]['filter'] is not None:
            filter &= domain_filters[domain]['filter']
        if usageFilters[usage] is not None:
            filter &= usageFilters[usage]
        var = ods.read(variable,filter).values()
        return var
