from configparser import SafeConfigParser

from semperpy.core.tools import nocasedict,is_list,is_string,to_list,dictionary
from semperpy.core.innerpython import InnerPython

#----------------------------------------------------------------------------
# SemperPy Copyright SynopticView, GMAO 2009-2010
#
# Claude Gibert, December 2009, dev@synopticview.com
#----------------------------------------------------------------------------
class ConfigFile(nocasedict):

    @staticmethod
    def mybool(value):
        value = value.lower()
        if value == 'false' or value == '0' or value == 'no':
            return False
        elif value == 'true' or value == '1' or value == 'yes':
            return True
        v = ['true','yes','1','false','no','0']
        raise ValueError("Valid values for a boolean are:\n" + ',\n'.join(v))
        

    def __init__(self,configfile,process_coma = True, overwrite = True):
        self.process_coma_ = process_coma
        configfile = to_list(configfile)
        configfile.reverse()
        if len(configfile) == 0:
            raise IOError('No configuration files were found')
        parser = SafeConfigParser()
        for file in configfile:
            if isinstance(file,str):
                parser.read(file)
            else:
                parser.readfp(id)
            if len(parser.sections()) == 0:
                raise IOError("Could not read " + file + " file")
            self.types_ = {}
            if parser.has_section('__types__'):
                for key,item in parser.items('__types__'):
                    if item == 'bool':
                        self.types_[key] = self.mybool
                    else:
                        self.types_[key] = InnerPython.get_class(item)
            parser.remove_section('__types__')

            for section in parser.sections():
                if (overwrite and section in self) or not section in self:
                    self[section] = nocasedict()
                for key,item in parser.items(section):
                    if key[0] != '_':
                        if not overwrite:
                            if key in self[section]:
                                self[section][key] = to_list(self[section][key])
                            else:
                                self[section][key] = []
                            self[section][key].append(self.clean_item(key,item,self.process_coma_))    
                        else:
                            self[section][key] = self.clean_item(key,item,self.process_coma_)

            for section in list(self.values()):
                for key,item in list(section.items()):
                    if is_list(item):
                        l = []
                        for v in item:
                            l.append(self.nested_sections(v))
                        section[key] = l
                    else:
                        section[key] = self.nested_sections(item)

    def clean_item(self,key,item,process_coma):
        if process_coma:
            v = item.split(",")
            v = [ x.strip() for x in v ]
        else:
            v = [item]
        if key in self.types_:
            translator = self.types_[key]
            v = [ translator(x) for x in v ]
        if len(v) == 1: v = v[0]
        return v
                    
    def nested_sections(self,item):
        #---------------------------------------------------------------
        # We can nest sections if in the right hand side a name is
        # between square brackets: [name]
        #---------------------------------------------------------------
        if is_string(item) and len(item) > 1 and item[0] == '[' and item[-1] == ']':
            name = item[1:-1] # need to remove the square brackets
            name = name.strip()
            if name in self:
                return self[name]
            else:
                return item
        else:
            return item
