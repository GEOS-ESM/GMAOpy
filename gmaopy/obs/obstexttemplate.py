import re
from collections import defaultdict
from semperpy.core.tools import to_list, is_string, is_list, no_list
from semperpy.core.date import Date
from semperpy.core.format import float10Power
from semperpy.core.configfile import ConfigFile
from semperpy.core.configure import Configure
from gmaopy.ods.parameter import Parameter
from gmaopy.stats.statistics import Statistics
from gmaopy.stats.stattexttemplate import StatTextTemplate

#---------------------------------------------------------------------------------------
# This is where data formatting for displaying titles, legends etc... happens.
# In the title, legend etc... templates (in json files), we define variables between
# <> e.g. <expver>. If the keyword is part of the directive being processed it is
# displayed, unless a method with the same name as the variable is defined here.
# That way, the normal formatting of data can be overriden and new keywords can be
# created (e.g. date_interval).
#---------------------------------------------------------------------------------------
class ObsTextTemplate(StatTextTemplate):

    def parameter(self,key,dir):
        if 'kt' in dir:
            kts = to_list(dir['kt']) 
            names = []
            for kt in kts:
                names.append(Parameter.shortname(kt))
            return ','.join(names)
        else:
            return ''

    def parameter_long(self,key,dir):
        if 'kt' in dir:
            kts = to_list(dir['kt']) 
            names = []
            for kt in kts:
                names.append(Parameter.title(kt))
            return ','.join(names)
        else:
            return ''

    def unit(self,key,dir,what = 'statistic'):
        if what in dir:
            stats = to_list(dir[what])
            all = []
            for stat in stats:
                actor = Statistics.create('obsstat',stat)
                unit = actor.unit()
                if unit is None:
                    if 'type' in dir:
                        if dir['type'] == 'im':
                            if 'variable' in dir and dir['variable'] == 'xvec':
                                unit = 'J/kg'
                    if unit is None:
                        unit = self.param_unit(key,dir)
                if not unit is None:
                    if unit != '':
                        unit = '(%s)' % unit 
                    all.append(unit)
            return ','.join(all)

    def colormap_unit(self,key,dir):
        return self.unit(key,dir,'colormap_statistic')

    def param_unit(self,key,dir):
        if 'kt' in dir:
            kts = to_list(dir['kt']) 
            names = []
            for kt in kts:
                names.append(Parameter.unit(kt))
            return ','.join(names)
        else:
            return ''

    def x_scatter_variable(self,key,dir):
        if 'variable' in dir:
            lt = dir['variable'][0]
            return self.beautify(key,dir,lt,'title')
        else:
            return ''

    def y_scatter_variable(self,key,dir):
        if 'variable' in dir:
            lt = dir['variable'][1]
            return self.beautify(key,dir,lt,'title')
        else:
            return ''

    def channel(self,key,dir):
        if not 'level' in dir:
            return ''
        if not 'levtype' in dir:
            return dir[key]
        levtype = no_list(dir['levtype'])
        if levtype != 'ch':
            return ''
        level = to_list(dir['level'])
        if len(level) > 1:
            return ''
        return 'Channel %d' % level[0]

    def coverage_variable(self,key,dir):
        return dir['variable'][2]

    #---------------------------------------------------------------------------------------
    # utilities
    #---------------------------------------------------------------------------------------
    def _beautify(self,key,dir,value,section = None):
        if value == 'xvec' and dir['type'] == 'im':
            return 'Impact'
        return super(ObsTextTemplate,self)._beautify(key,dir,value,section)
