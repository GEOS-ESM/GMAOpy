import os.path
from collections import defaultdict
from semperpy.core.tools import nestedLoops, to_list
from semperpy.core.configfile import ConfigFile
from semperpy.core.configure import Configure
from semperpy.directive.directive import Directive

class PlotData(Directive):

    cache_ = defaultdict(dict)

    def __init__(self,*args,**kwargs):
        self.config_ = self.readConfiguration()
        super(PlotData,self).__init__(*args,**kwargs)

    def startRetrieve(self):
        pass

    def stopRetrieve(self):
        pass

    def distribute(self,owner,what):
        combinable = self.combinable(what)
        self.keepTrackOfDefaults(False)
        result = nestedLoops(self,combinable)
        self.keepTrackOfDefaults(True)
        return result

    def prefixName(self):
        return None,None

    def readConfiguration(self):
        prefix, name = self.prefixName()
        if not prefix in self.cache_ or not name in self.cache_[prefix]:
            configure = Configure(prefix)
            files = configure.file(name,'CONFIG','plot')
            self.cache_[prefix][name] = ConfigFile(files)
        return self.cache_[prefix][name]

    def combinable(self,what):
        return [ x for x in to_list(self.config_[what]['combinable']) if x in self ]

    def columns(self,what):
        return to_list(self['_columns'])

    def index_columns(self,what):
        #import sys
        #callingframe = sys._getframe(1)
        #print 'My caller is the %r function in a %r class' % (callingframe.f_code.co_name, callingframe.f_locals['self'].__class__.__name__)
        #print 'semperpy/plot/plotdata'
        if 'index_columns' in self.config_[what]:
            #print 'index columns: ',to_list(self.config_[what]['index_columns'])
            return to_list(self.config_[what]['index_columns'])
        else:
            return []

    def draw_index_columns(self,what):
        if 'draw_index_columns' in self.config_[what]:
            return to_list(self.config_[what]['draw_index_columns'])
        else:
            return self.index_columns(what)

    def title(self,what):
        return to_list(self.config_[what]['title'])

    def xtitle(self,what):
        return self.config_[what]['xtitle']

    def ytitle(self,what):
        return self.config_[what]['ytitle']

    def colorbartitle(self,what):
        return self.config_[what]['colorbartitle']

    def legend(self,what):
        return self.config_[what]['legend']

    def missingValue(self):
        return 1.7E38

    def moreIsBetter(self):
        return False

    def colorMapMoreIsBetter(self):
        return False

    def createTextTemplate(self):
        return TextTemplate()

    def printout(self,main,what):
        what(main,self)

    def __copy__(self):
        c = super(PlotData,self).__copy__()
        c.config_ = self.config_
        return c

plotdata = PlotData
