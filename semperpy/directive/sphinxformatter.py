import re
from semperpy.directive.help import Help, Formatter
from semperpy.core.tools import is_list, is_dict, find_variables, to_list, apply_type
from semperpy.core.date import Date
from semperpy.core.innerpython import InnerPython

class SphinxFormatter(Formatter):
    
    column_width = 20

    def heading(self,r,title,char):
        r.append(title)
        r.append(char * len(title))
        r.append('')
        return r

    def build_separator(self,char,colwidth,columns):
        segment = '+' + char * (colwidth - 1)
        return segment * len(columns) + '+'

    def build_row(self,colwidth,columns):
        segments = []
        for c in columns:
            c = str(c)
            segments.append('|' + c + ' ' * (colwidth - len(c) - 1))
        return ''.join(segments) + '|'

    def bold(self,text):
        return '**%s**' % text

    def italics(self,text):
        if text == '':
            return ''
        return '*%s*' % text

    def summaryTable(self,r,directive):
        keywords = [ x for x in directive['order'] if x in directive['keywords'] ]
        maxlength = 0
        for keyword in keywords:
            if len(keyword) > maxlength:
                maxlength = len(keyword)
            item = directive['keywords'][keyword]
            if 'default_value' in item:
                ll = len(str(item['default_value']))
                if ll > maxlength:
                    maxlength = ll
            for v in item['keys']:
                name,value = v
                if len(name) > maxlength:
                    maxlength = len(name)
                value = to_list(value)
                for v in value:
                    ll = len(str(v))
                    if ll > maxlength:
                        maxlength = ll
        header = ['keyword','default','attribute','value']
        lengths = [ len(x) for x in header ]
        m = max(lengths)
        if m > maxlength:
            maxlength = m
        colwidth = maxlength + 6
        r.append(self.build_separator('-',colwidth,header))
        r.append(self.build_row(colwidth,header))
        r.append(self.build_separator('=',colwidth,header))
        for keyword in keywords:
            item = directive['keywords'][keyword]
            r.append(self.build_row(colwidth,[self.bold(keyword),item['default_value'],'','']))
            r.append(self.build_separator('-',colwidth,header))
            for v in item['keys']:
                name,value = v
                value = to_list(value)
                for v in value:
                    r.append(self.build_row(colwidth,['','',self.italics(name),str(v)]))
                    r.append(self.build_separator('-',colwidth,header))
                    name = ''
            r.append(self.build_separator('-',colwidth,header))
        r.append('')
        return r

    def directive(self,directive):
        r = []
        title = directive['name']
        r = self.heading(r,title,'=')
        if directive['help']:
            r.append(self.help(directive['help']))
            r.append('')
        for key in ['inherit_from','specialize_from','post_validate']:
            if key in directive:
                r.append('**%s**: %s' % (key,directive[key]))
                r.append('')
        r = self.heading(r,'Summary','-')
        r = self.summaryTable(r,directive)
        r = self.heading(r,'Keywords','-')
        for keyword in directive['order']:
            if keyword in directive['keywords']:
                item = directive['keywords'][keyword]
                r = self.heading(r,keyword,'^')
                default= item['default_value']
                if is_list(default):
                    default = apply_type(str,default)
                    default = ', '.join(default)
                else:
                    default = str(default)
                if default == '':
                    default = '""'
                r.append('default: ' + self.bold(default))
                r.append('')
                if item['help']:
                    r.append(self.help(item['help']))
                    r.append('')
                header = ['attribute','value']
                colwidth = 50
                if len(item['keys']) > 0:
                    r.append(self.build_separator('-',colwidth,header))
                    r.append(self.build_row(colwidth,header))
                    r.append(self.build_separator('=',colwidth,header))
                    for v in item['keys']:
                        name,value = v
                        if is_list(value):
                            for v in value:
                                r.append(self.build_row(colwidth,[name,v]))
                                r.append(self.build_separator('-',colwidth,header))
                                name = ''
                        else:   
                            value = str(value)
                            r.append(self.build_row(colwidth,[name,value]))
                            r.append(self.build_separator('-',colwidth,header))
                    r.append('')
        d = Date()
        r.append('generated on %s' %d)
        return '\n'.join(r)

    def help(self,value):
        value = ' '.join(value)
        keywords = find_variables(value)
        for keyword in keywords:
            value = re.sub('<%s>' % keyword,"**%s**" % keyword,value)
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

    def list(self,all):
        return "Directive list: \n    %s" % '\n    '.join(all)

Help.register('sphinxformatter',SphinxFormatter)
