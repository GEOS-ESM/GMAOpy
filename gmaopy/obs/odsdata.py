from semperpy.core.tools import to_list
from semperpy.plot.document import document
from semperpy.plot.dimension import Dimension
from gmaopy.obs.obsplotdata import ObsPlotData
from gmaopy.obs.obsexpander import ObsExpander
from gmaopy.obs.obstexttemplate import ObsTextTemplate

class ODSData(ObsPlotData):

    def __init__(self,*args,**kwargs):
        super(ODSData,self).__init__(*args,**kwargs)
        self.variables_ = {}

    def hasVariable(self,variable):
        return variable in self.variables_

    def variables(self,value = None, variable = None):
        if variable is None:
            variable = self['variable']
        elif variable == 'all':
            return self.variables_
        if value is not None:
            self.variables_[variable] = value
        return self.variables_[variable]
    
    def distribute(self,owner,what):
        isDoc = isinstance(owner,document)
        result = []
        s = set()
        if 'filename' in self:
            all = ObsExpander.expand_for_ods_retrieval(self,s)
            if isDoc:
                self.assignLevels(all)
            for one in all:
                one['usage'] = to_list(one['usage'])
                result += one.distribute(owner,what)
        else:
            if not isDoc:
                self.assignLevels([self])
            result =  super(ODSData,self).distribute(owner,what)
            if 'kx' in self and 'kt' in self:
                result = ObsExpander.expand_for_ods_retrieval(result,s)
            else:
                result = ObsExpander.assign_ids(result)
        if not isDoc:
            self.assignLevels(result)
        return result

    def __copy__(self):
        new = super(ODSData,self).__copy__()
        new.variables_ = dict(self.variables_)
        return new

    def prefixName(self):
        return 'SEMPERPY','odstitles.def'

    def doRetrieve(self,owner,what):
        axis_name = self.draw_index_columns(what)
        """
        We call the prepare_values method on the dimension we plot against
        (e.g. level, date) to have a chance to sort the values in the order
        we want for a particular plot.
        """
        for name in axis_name:
            if name != '':
                index_dimension = Dimension.createDimensionFilter(name,what)
                self[name] = index_dimension.prepare_values(self,self[name])

odsdata = ODSData
