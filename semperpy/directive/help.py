import re
from semperpy.core.decorators import abstractMethod
from semperpy.core.tools import is_list, find_variables, no_list
from semperpy.core.innerpython import InnerPython
from semperpy.language.languagedefinition import LanguageDefinition
from semperpy.directive.directive import Directive

class Formatter(object):
    
    @abstractMethod
    def directive(self,directive):
        pass

    def variables(self,value):
        return find_variables(value)

    def actions(self,value):
        return [ x for x in re.findall('\{(.*?)\}',value) ]

    def run_action(self,action):
        result = None
        all = action.split('(')
        action = all[0]
        args = []
        if len(all) > 1:
            # get rid of )            
            a = all[1][0:-1]
            args = a.split(',')
        what = InnerPython.get_class(action)
        if what:
            result = what(*args)
        return result

class Help(object):

    factory_ = {}

    @classmethod
    def register(self,name,what):
        self.factory_[name]= what

    def create(self,name):
        return self.factory_[name]()

    def __init__(self,application = 'semperpy'):
        self.application_ = application

    def __call__(self,directive = None,format = 'ascii'):
        formatter = self.create(format)
        dir = Directive()
        if directive is None:
            all = dir.allDirectives(self.application_)
            return formatter.list(all)
        else:
            newdir = {}
            l = dir.language(directive)
            help = l.get('help','') 
            newdir['name'] = l['directive']
            newdir['help'] = help
            for key in ['inherit_from','specialize_from','post_validate']:
                if key in l:
                    newdir[key] = l[key]
            newdir['keywords'] = {}
            keys = l['keywords']
            keywords = list(keys.keys())
            keywords.sort()
            newdir['order'] = keywords
            valid = [ x for x in LanguageDefinition.keywords()['valid'] if (x != 'help' and x != 'default_value') ]
            valid.sort()
            for key in keywords:
                # if the keyword is removed at the level of the directive definition we are
                # displaying, we don't show that keyword
                if key[0] != '_' and not ('remove' in keys[key] and keys[key]['remove']):
                    item = {}
                    item['default_value'] = keys[key].get('default_value',None)
                    item['help'] = keys[key].get('help','')
                    item['keys'] = []
                    for v in valid:
                        if v in keys[key]:
                            item['keys'].append((v,keys[key][v]))
                    newdir['keywords'][key] = item
            return formatter.directive(newdir)

