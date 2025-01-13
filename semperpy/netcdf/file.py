import copy
import numpy as np
import numpy.ma as ma
from netCDF4 import Dataset
from semperpy.core.date import Date
from semperpy.slicing.slicer import Slicer
from semperpy.slicing.cf10.cf10metadata import CF10MetaData
from semperpy.slicing.slice2array import Slice2Array
from semperpy.slicing.slice2list import Slice2List
from semperpy.netcdf.fieldcreator import FieldCreator

class File(object):

    dimensionFactory_ = {
    }
    handler_ = CF10MetaData()

    @classmethod
    def registerDimension(self,name,official_name,class_instance,metadata_handler=None):
        if not metadata_handler:
            metadata_handler = self.handler_
        self.dimensionFactory_[name] = dict(
            class_instance  = class_instance,
            handler         = metadata_handler,
            official_name   = official_name
        )

    def __init__(self,filename,verbose=0):
        try: 
            self.file_ = Dataset(filename)
        except:
            raise IOError('Cannot open filename %s' % (filename))
        self.variables_ = self.createVariableMap(self.file_)

        # Create axes (dimension objects which will deal with slicing data)
        self.dimensions_ = {}
        for dimension in self.file_.dimensions:
            self.dimensions_[dimension] = self.createDimension(dimension,self.variables_[dimension])
            if verbose > 0:
                print(self.dimensions_[dimension])

    def dimensions(self):
        return [ self.dimensions_[x] for x in self.file_.dimensions ]

    def createDimension(self,dimension,variable):
        if not dimension in self.dimensionFactory_:
            raise IndexError('unknown dimension name in netCDF file reader, known dimensions: \n   %s' % ('\n   '.join(list(self.dimensionFactory_.keys()))))
        handler = self.dimensionFactory_[dimension]['handler']
        return self.dimensionFactory_[dimension]['class_instance'](dimension,self.dimensionFactory_[dimension]['official_name'],variable,handler)

    def createVariableMap(self,file):
        # We need to overcome a problem, variable names in the netcdf file are case sensistive,
        # sometimes it's uppercase sometimes not (changes between opendap and direct access).
        # The user shouldn't need to be aware of this do we need to make a indirection.
        variables = {}
        for k,i in list(file.variables.items()):
            l = k.lower()
            L = k.upper()
            is_upper = L == k
            if l in variables:
                l = l + '_upper'
                L = L + '_UPPER'
            variables[l] = i
            variables[L] = i
        return variables

    def slice(self,varname,directive,visitor,**kargs):
        if not varname in self.variables_:
            raise IndexError('Variable %s was not found in this file' % varname)
        variable = self.variables_[varname]
        dimensions = [ self.dimensions_[x] for x in variable.dimensions ]
        slicer = Slicer(dimensions)
        slicer(variable,directive,visitor,**kargs)

    def readVariable(self,variableName):
        return

    def readArray(self,directive,generator = None,squeeze = False,**kargs):
        array = Slice2Array(generator)
        self.slice(directive['variable'],directive,array,**kargs)
        if squeeze:
            return array.squeezedArray()
        else:
            return array.array()

    def readFieldSet(self,directive,visitor = None,**kargs):
        if not visitor:
            visitor = FieldCreator()
        list = Slice2List(visitor)
        self.slice(directive['variable'],directive,list,**kargs)
        return list.fieldSet()
    readBundle = readFieldSet
