import re
from semperpy.core.tools import substitute_variable_list,find_variables,apply_type,is_list

class NameGenerator(object):

    def __call__(self,plots,filename,info):
        variables = find_variables(filename)
        sub = {}
        for var in variables:
            values = []
            done = set()
            if var in info:
                value = self.cleanup(info[var])
                if not value in done:
                   values.append(value)
                done.add(value)
            sub[var] = '_'.join(values)
        filename = substitute_variable_list(variables,filename,sub)
        filename = substitute_variable_list(variables,filename,info)
        filename = re.sub(' ','_',filename)
        filename = re.sub('^_','',filename)
        filename = re.sub('__','_',filename)
        filename = re.sub('_\.','.',filename)
#        filename = filename.lower()
        return filename

    def cleanup(self,value):
        value = apply_type(str,value)
        if is_list(value):
            value = '-'.join(value)
        return value
