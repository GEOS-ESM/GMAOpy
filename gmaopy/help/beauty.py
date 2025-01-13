import sys
from semperpy.core.date import Date
from semperpy.core.configure import Configure
from semperpy.core.configfile import ConfigFile
from gmaopy.help.helpsystem import HelpSystem

class Beauty(object):
    
    def __init__(self,format,*args):
        self.section_ = None
        if len(args) > 0:
            self.section_ = args[0]

    def __call__(self):
        config = Configure('semperpy')
        c = ConfigFile(config.file('beauty.def','CONFIG','main'),process_coma=False)
        if self.section_ is not None:
            if not self.section_ in c:
                sys.stderr.write("No section called '%s' in the Beautifer\n\n" % self.section_)
                exit(1)
            sections = [self.section_]
        else:
            sections = list(c.keys())
            sections.sort()
        help = []
        empty = [' ']
        for section in sections:
            l = c[section]
            help.append('section: %s:' % section)
            all = list(l.keys())
            all.sort()
            for entry in all:
                help.append('    %s: %s' % (str(entry).ljust(20), str(l[entry])))
            help += empty
        title = ['Beautifier:'] + empty
        d = Date()
        tail = empty + ['generated on %s' % d] + empty
        return title + help + tail


HelpSystem.register_module('beauty',Beauty)
