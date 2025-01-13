#----------------------------------------------------------------------------
# SemperPy Copyright GMAO 2009-2011
#
# Author: Claude Gibert, May 2011, claude.gibert@synopticview.com
#-------------------------------------------------------------------
class CF10MetaData(object):

    """
        Implements a metadata handler like one passed to 
        slicer.dimensions.dimension.Dimension.
        If the object has a method with the name "name", the
        method is called, otherwise we assume the variable in the dimension
        (probably netCDF) has an attribute with that name.

        This enables to assume that the variable has an attribute with the name,
        if not or if we want to specialize the behaviour for one particular
        attribute, we define a method with that name.
    """

    def __call__(self,dimension,name):
        try:
            f = getattr(name,self)
            return f(dimension,name)
        except:
            pass
        return getattr(dimension.variable_,name)
