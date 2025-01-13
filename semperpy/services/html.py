#----------------------------------------------------------------------------
# SemperPy Copyright GMAO 2009-2010
#
# Claude Gibert, May 2010, dev@synopticview.com
#-------------------------------------------------------------------
import re
import os

from semperpy.core.tools import apply_type, is_list, to_list

class HTML(object):

    templates = {}
    path = None

    @staticmethod
    def list(items):
        ret = []
        for x in items:
            if is_list(x):
                x = HTML.list(x)
                # we don't specify <li></li> if there is a sublist.
                ret.append("%s" % x)
            else:
                ret.append("<li>%s</li>" % x)
        return "<ul>%s</ul>" % '\n'.join(ret)

    @classmethod
    def webPath(self):
        if not self.path:
            self.path = os.environ['SEMPERPY_WEB']
            if self.path[-1] != '/':
                self.path += '/'
        return self.path

    @classmethod
    def templatePath(self):
        return self.webPath() + 'templates'

    @classmethod
    def cssPath(self):
        return self.webPath() + 'css'

    @classmethod
    def template(self,name):
        if not name in self.templates:
            f = open(self.templatePath() + '/' + name + '.tmpl')
            t = f.read()
            f.close()
            self.templates[name] = t
        return self.templates[name]

    @classmethod
    def keywords(self,text):
        return [ re.sub('__','',x) for x in re.findall('__.*?__',text)]

    @classmethod
    def substituteVariables(self,template_name,**kargs):
        template = self.template(template_name)
        for keyword in kargs:
            k = apply_type(str,kargs[keyword])
            if is_list(k):
                k = self.list(k)
            template = re.sub('__'+ keyword + '__',k,template)
        return template
