import re
from semperpy.core.tools import is_list
from semperpy.core.date import Date
from semperpy.directive.help import Help, Formatter

class ASCIIFormatter(Formatter):
    
    tab = '   '

    def directive(self,directive):
        r = []
        r.append('directive: %s' % directive['name'])
        if directive['help']:
            r.append(self.help(directive['help']))
            r.append('')
        for keyword in directive['order']:
            if keyword in directive['keywords']:
                item = directive['keywords'][keyword]
                r.append('%skeyword: %s   default: %s' % (self.tab,keyword,item['default_value']))
                if item['help']:
                    r.append(self.help(item['help']))
                for v in item['keys']:
                    name,value = v
                    if is_list(value):
                        value = ','.join([ str(x) for x in value])
                    else:   
                        value = str(value)
                    r.append('%s%s = %s' % (self.tab * 2,name,value))
                r.append('')
        d = Date()
        r.append('generated on %s' %d)
        return '\n'.join(r)

    def help(self,value):
        tab = self.tab
        value = '\n'.join([ tab + x for x in value ])
        keywords = self.variables(value)
        for keyword in keywords:
            value = re.sub('<%s>' % keyword,"'%s'" % keyword,value)
        actions = self.actions(value)
        for action in actions:
            s = self.run_action(action)
            if s is not None:
                action = re.sub('\(','\\(',action)
                action = re.sub('\)','\\)',action)
                if is_list(s):
                    s = ', '.join(s)
                value = re.sub('{%s}' % action,str(s),value)
        return value
    __call__ = help

    def list(self,all):
        all.sort()
        return '\n'.join(all)

Help.register('ascii',ASCIIFormatter)
