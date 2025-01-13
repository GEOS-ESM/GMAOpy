#----------------------------------------------------------------------------
# SemperPy Copyright GMAO 2009-2011
#
# Author: Claude Gibert, February 2011, claude.gibert@synopticview.com
#-------------------------------------------------------------------
from semperpy.core.tools import specialise
from semperpy.slicing.dimensions.dimension import Dimension
from semperpy.slicing.dimensions.sorteddescending import SortedDescendingDimension
from semperpy.slicing.dimensions.sortedascending import SortedAscendingDimension

class LevelDimensionDescending(SortedDescendingDimension):
    pass

class LevelDimensionAscending(SortedAscendingDimension):
    pass

class LevelDimension(Dimension):

    def __init__(self,name,official_name,variable,metadata_handler = None):
        newclass = LevelDimensionAscending
        if len(variable) > 1:
            if variable[1] < variable[0]:
                newclass = LevelDimensionDescending
        specialise(self,newclass)
        super(newclass,self).__init__(name,official_name,variable,metadata_handler)
