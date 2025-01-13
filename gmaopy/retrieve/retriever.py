import copy
import re
from collections import defaultdict
from semperpy.core.tools import substitute_variables, substitute_unix_calculated_dates,resolve_environment_variables, to_list
from semperpy.core.date import Date
from semperpy.core.dategroup import DateGroup
from semperpy.core.configfile import ConfigFile
from semperpy.core.configure import Configure
from semperpy.archive.archive import Archive

class Retriever(object):

    cache_ = {}

    def __init__(self,prefix,grouping,directives):
        self.configure_ = Configure(prefix)
        result = defaultdict(dict)
        for directive in directives:
            if not 'location' in directive:
                directive['location'] = directive['source']
            self.config_ = self.configuration(directive['location'],self.configure_)
            result = self.filename(directive,result)
        args = grouping.split(':')
        arg = 1
        if len(args) > 1:
            arg = int(args[1])
        self.files_ = DateGroup.createGroup(args[0],result,arg)

    def filename(self,directive,result):
        directive, location, archive_type = self.build_path(directive,self.config_)
        dir = dict(directive)
        files = defaultdict(list)
        for file in to_list(directive['collection']):
            dir['collection'] = file
            name = substitute_variables(location,dir)
            for date in to_list(directive['date']):
                files[date].append(substitute_unix_calculated_dates(name,Date(date)))
        for date in to_list(directive['date']):
            currentfile = tuple(files[date])
            if not currentfile in result[date]:
                result[date][currentfile]=dict(archive_type=archive_type,directive=[])
            result[date][currentfile]['directive'].append(directive)
        return result

    @classmethod
    def configuration(self,name,configure):
        configfile = configure.file(name + '.def','CONFIG','retrieve')
        hash = ','.join(configfile)
        if not hash in self.cache_:
            config = ConfigFile(configfile)
            self.cache_[hash] = config
        else:
            config = self.cache_[hash]
        return config

    @classmethod
    def build_path(self,directive,config):
        data = {}
        type = directive['type']
        for k in config[type]:
            if k in directive:
                data[k] = directive[k]
            else:
                data[k] = config[type][k]
        root = data['root_tmpl']
        tree = data['tree_tmpl']
        file = data['file_tmpl']
        archive_type = data['archive_type']
        location = root + '/' + tree + '/' + file
        # some custom cooking just because of history
        if directive['type'] == 'im':
            expver = directive['expver']
            directive['d1'] = expver[1]
            directive['d2'] = expver[2]
            directive['d3'] = expver[3]
            version = re.search('(p[0-9]+)',expver)
            if version:
                directive['d3'] += '_' + version.group()
        return directive, location, archive_type

    @classmethod
    def datedFile(self,directive,prefix):
        configure = Configure(prefix)
        if 'location' in directive:
            location = directive['location']
        else:
            location = directive['source']
        config = self.configuration(location,configure)
        directive, location, archive_type = self.build_path(directive,config)
        dir = dict(directive)
        name = substitute_variables(location,dir)
        date = to_list(directive['date'])[0]
        return substitute_unix_calculated_dates(name,Date(date))

    @classmethod
    def full_path(self,directive,prefix):
        configure = Configure(prefix)
        if 'location' in directive:
            location = directive['location']
        else:
            location = directive['source']
        config = self.configuration(location,configure)
        directive, location, archive_type = self.build_path(directive,config)
        location = substitute_variables(location,directive)
        date = to_list(directive['date'])[0]
        dated_name = substitute_unix_calculated_dates(location,Date(date))
        l = dated_name.split('/')
        return '/'.join(l[:-1])

    @classmethod
    def retrieve(self,files,archive_type):
        stage = defaultdict(list)
        for i,file in enumerate(files):
            t = archive_type[i]
            stage[t].append(file)
        for archive,files in list(stage.items()):
            a = Archive.create(archive,files) 
            a.stage()

    def files(self):
        iterator = self.files_.iterator()
        for group in iterator:
            for date,files in group:
                f = list(files.keys())
                flattened = []
                archive_type = []
                for x in f:
                    for y in x:
                        flattened.append(y)
                        archive_type.append(files[x]['archive_type'])
            self.retrieve(flattened,archive_type)
            for date,files in group:
                yield date,files
