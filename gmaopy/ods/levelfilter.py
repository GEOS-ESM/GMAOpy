from semperpy.observations.obsfilter import ObsFilter

class LevelFilter(ObsFilter):

    def __init__(self,value = None, levelist = None, filename = None):
        self.levelist_ = levelist
        self.filename_ = filename
        super(LevelFilter,self).__init__(value)

    def levelist(self):
        return self.levelist_

    def filename(self):
        return self.filename_
