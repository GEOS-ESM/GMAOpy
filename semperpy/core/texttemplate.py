import re
from semperpy.core.tools import mergedicts_overwrite, find_variables, substitute_variable_list, is_list, no_list

class TextTemplate(object):

    def processText(self,template,directive,section = None,remove_empty_lines=True,**kwargs):
        dir = mergedicts_overwrite(directive,kwargs)
        vars = {}
        variables = find_variables(template)
        for key in variables:
            vars[key] = self.getText(key,dir,section)
        text =  substitute_variable_list(variables,template,vars)
        if remove_empty_lines:
            text = re.sub('\n\s*\n+','\n',text)
        # remove double spaces
        text = re.sub('  ',' ',text)
        # remove trailing spaces
        text = re.sub(' $','',text)
        # remove trailing coma
        text = re.sub(',$','',text)
        return text

    def getText(self,key,dir,section = None,beauty = True):
        result = ''
        try:
            method = getattr(self,key)
            result = method(key,dir)
        except AttributeError:
            if key in dir:
                result = dir[key]
        if is_list(result) and len(result) == 1:
            result = no_list(result)
        if beauty:
            return self.beautify(key,dir,result,section)
        else:
            return result

    def beautify(self,key,dir,value,section):
        return value

    def despatchVariables(self,a,b,directive):
        va = set(find_variables(a))
        vb = set(find_variables(b))
        v = va.intersection(vb)
        for key in v:
            value = self.getText(key,directive,beauty = False)
            if value != '':
                if is_list(value) and len(value) > 1:
                    a = re.sub('<%s>' % (key),'',a)
                else:
                    b = re.sub('<%s>' % (key),'',b)
            else:
                a = re.sub('<%s>' % (key),'',a)
        a = re.sub('  ',' ',a)
        b = re.sub('  ',' ',b)
        return a.strip(),b.strip()
    dispatchVariables = despatchVariables
