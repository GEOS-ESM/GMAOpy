#----------------------------------------------------------------------------
# SemperPy Copyright GMAO 2009-2012
#
# Author: Claude Gibert, February 2011, claude.gibert@synopticview.com
#-------------------------------------------------------------------
class Slicer(object):

    def __init__(self,dimensions):
        self.names_ = [ x.officialName() for x in dimensions ]
        self.dimensions_ = dimensions

    def __call__(self,variable,directive,visitor,verbose = 0,**kargs):
        dimensions = self.dimensions_
        shape = []
        slices = []
        metadata = []
        is_interval = []
        # go over all dimensions
        for i in range(len(self.names_)):
            name = self.names_[i]
            dimension = self.dimensions_[i]
            this_metadata = []
            # pick values specified by the directive. No specification means take all 
            # available values
            if name in directive:
                value = directive[name]
            else:
                value = {}
            # the axes returns the slice(s) to be taken from the variable
            s = dimension.findSlice(value,is_interval)
            # we also want to hold the corresponding dimension's meta-data 
            for aslice in s:
                this_metadata += dimension.slice(aslice)
            # calculate the size of the slice along that dimension
            # and add it to the shape
            dimlength = 0
            for sl in s:
                dimlength += sl.stop - sl.start
            shape.append(dimlength)
            # we remember all the required slices and meta-data values
            slices.append(s)
            metadata.append(this_metadata)
        if verbose > 0:
            print("requested shape:",shape)
            if verbose > 9:
                print("slices:",slices)
                print("meta-data:",metadata[0:-2])
        visitor.preProcess(self.dimensions_,variable,shape,slices,metadata)
        self.slice(self.names_,variable,slices,metadata,is_interval,visitor,**kargs)
        visitor.postProcess(self.dimensions_,variable,shape,slices,metadata)
        if verbose > 0:
            print()
        
    def slice(self,dimensions,variable,slices,metadata,is_interval,visitor,index = 0,src=[],dst=[],meta=[],**kargs):
        if len(slices) == 0:
            if len(src) != len(dst) or len(src) != len(meta):
                ValueError('An error occurred, lengths of arrays are inconsistent')
            visitor(dimensions,variable,src,dst,meta,is_interval,**kargs)
        else:
            value = slices[0]
            start = 0
            i = 0
            d = []
            for v in value:
                vlen = v.stop - v.start
                dest = slice(start,start + vlen,v.step)
                start += vlen
                d.append(dest)
            m = metadata[0]
            if is_interval[index]:
                self.slice(dimensions,variable,slices[1:],metadata[1:],is_interval,visitor,index + 1,src + [value],dst + [d],meta+[m],**kargs)
            else:
                for i in range(len(value)):
                    self.slice(dimensions,variable,slices[1:],metadata[1:],is_interval,visitor,index + 1,src + [[value[i]]],dst + [[d[i]]],meta+[[m[i]]],**kargs)
