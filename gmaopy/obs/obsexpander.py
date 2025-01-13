import copy
import re
from semperpy.core.configfile import ConfigFile
from semperpy.core.tools import apply_type, to_list, is_list
from gmaopy.ods.odsinfo import ODSInfo
from gmaopy.retrieve.retriever import Retriever

class ObsExpander(object):

    id_ = 0

    @classmethod
    def expand_for_storage(self,obs,unique):
        obs = self.gatherObservations(obs)
        all = []
        for o in obs:
            triplets = self.distributeKxKt(o,unique)
            if len(triplets) > 0:
                all += self.distributeObservations(o,triplets)
        for i in range(len(all)):
            all[i] = self.insertInfo(all[i])
            all[i] = self.insertFiles(all[i])
        return all

    @classmethod
    def expand_for_retrieval(self,obs):
        all = self.gatherObservations(obs)
        for i in range(len(all)):
            all[i] = self.insertInfo(all[i])
        return all

    @classmethod
    def expand_for_ods_retrieval(self,obs,unique):
        all = []
        if not is_list(obs):
            obs = self.gatherObservations(obs)
        self.assign_ids(obs)
        for o in obs:
            # this is different from expand_for_storage because
            # we are plotting and there could be duplicate kx, kt
            # combinations for different domains or dates etc..
            # so we sabotage the unicity by creating a new set
            # every time.
            unique = set()
            o['o_kt'] = o['kt']
            o['o_kx'] = o['kx']
            triplets = self.distributeKxKt(o,unique)
            if len(triplets) > 0:
               all += self.distributeObservations(o,triplets)
        for i in range(len(all)):
            all[i] = self.insertInfo(all[i])
            all[i] = self.insertFiles(all[i])
        return all

    @classmethod
    def assign_ids(self,obs):
        for o in obs:
            if not '_id' in o:
                o['_id'] = self.id_
                self.id_ += 1
        return obs

    @classmethod
    def extractDefinition(self,obs):
        # if we are using a configuration file, let's first build
        # a list of observations from the file
        files = []
        groups = []
        obsgroup = obs.get('obsgroup',[])
        filename = obs.get('filename',[])
        if obsgroup != [] or filename != []:
            if 'kt' in obs or 'kx' in obs:
                raise ValueError('Defining both a filename and kt or kx is ambiguous')
            filenames = filename
            if len(filename) == 0:
                filenames.append('default_file')
            if obsgroup != [] and filename != []:
                if len(filenames) == 1:
                    if len(obsgroup) > 1:
                        obsgroup = [obsgroup]
                if len(obsgroup) != len(filename):
                    raise ValueError('The keywords obsgroup and filename should have the same lenth, found: %d and %d' % (len(obsgroup),len(filename)))
            if len(obsgroup) == 0:
                obsgroup = None
            for i in range(len(filenames)):
                file = filenames[i]
                config = ConfigFile(file)
                keys = list(config.keys())
                if obsgroup is not None:
                    if len(obsgroup[i]) != 0:
                        keys = obsgroup[i]
                keys.sort()
                files.append(file)
                groups.append(keys)
        return files,groups

    @classmethod
    def gatherObservations(self,obs):
        files,groups = self.extractDefinition(obs)
        expanded = []
        if len(files) > 0:
            info = ODSInfo()
            for i,file in enumerate(files):
                config = ConfigFile(file)
                keys = groups[i]
                for key in keys:
                    newobs = self.assign(config[key],copy.copy(obs),info)
                    if newobs is not None:
                        newobs['name'] = key
                        del newobs['filename']
                        expanded.append(newobs)
        elif not 'kt' in obs and not 'kx' in obs:
            expanded = self.all_observations(obs)
        else:
            expanded.append(obs)
        return expanded

    @classmethod
    def distributeObservations(self,obs,triplets):
        expanded = []
        for kx,kt,usage in triplets:
            new = copy.copy(obs)
            new['kx'] = kx
            new['kt'] = kt
            new['usage'] = usage
            expanded.append(new)
        return expanded

    @classmethod
    def distributeKxKt(self,obs,unique):
        info = ODSInfo()
        expanded = []
        kts = to_list(obs['kt'])
        if len(kts) == 0:
            kts = [-1]
        kxs = to_list(obs['kx'])
        if len(kxs) == 0:
            kxs = [-1]
        for kx in kxs:
            if kx != -1:
                for kt in kts:
                    if kt != -1 and kt in info.kx(kx):
                        for usage in obs['usage']:
                            hash = str(kx * 10000 + kt) + usage
                            if not hash in unique:
                                expanded.append([kx,kt,usage])
                                unique.add(hash)
        return expanded

    @classmethod
    def insertInfo(self,obs):
        levtype, levels = self.levelsOf(obs,obs['kx'],obs['kt'])
        if levels is not None and (not 'level' in obs or obs['level'] == 'all'):
            obs['level'] = levels
        if levtype is not None:
           obs['levtype'] = levtype
        return obs

    @classmethod
    def levelsOf(self,obs,kx,kt):
        info = ODSInfo()
        if not is_list(kx) and not is_list(kt):
            return info.levelsOf(kx,kt)
        else:
            return None,None

    @classmethod
    def insertFiles(self,obs):
        info = ODSInfo()
        files = info.fileNameOf(obs['kx'],obs['kt'])
        obs['collection'] = files
        return obs

    @classmethod
    def assign(self,item,obs,info):
        if 'database' in item:
            obs['database'] = item['database']
        if 'rank' in item:
            obs['rank'] = item['rank']
        for key in ['kx','kt']:
            if key in item:
                obs[key] = apply_type(int,to_list(item[key]))
            else:
                obs[key] = []
        kts = set()
        kxs = set()
        for kx in obs['kx']:
            for kt in obs['kt']:
                if info.knows(kx,kt):
                    kxs.add(kx)
                    kts.add(kt)
        if len(kts) == 0 and len(kxs) == 0:
            return None
        obs['kx'] = list(kxs)
        obs['kt'] = list(kts)
        if 'level' in item:
            l = item['level']
            if is_list(l):
                obs['level'] = apply_type(float,l)
            else:
                match = re.match('(.*?)to(.*?)by(.*)$',l)
                if match:
                    begin,end,step = [ int(x.strip()) for x in match.groups() ]
                    end += step
                    obs['level'] = list(range(begin,end,step))
                else:
                    obs['level'] = int(l)
        return obs

    @classmethod
    def all_observations(self,obs):
        result = []
        info = ODSInfo()
        kts = info.kts()
        for kt in kts:
            o = copy.copy(obs)
            o['kt'] = kt
            o['kx'] = list(info.kt(kt))
            o.checkLanguage()
            result.append(o)
        return result
