import numpy as np
from semperpy.core.tools import to_list
from semperpy.fields.containers.container import Container
from semperpy.slicing.arraygenerator import ArrayGenerator

class SliceContainer(Container):
    def __init__(self,array,slice,shape,**kargs):
        self.array_ = array
        self.slice_ = slice
        self.data_ = None
        self.params_ = kargs
        self.shape_ = shape

    def shape(self):
        return self.shape_

    def __call__(self):
        self.data_ = self.load()
        return self.data_

    def isLoaded(self):
        return self.data_ is not None

    def unload(self):
        self.data_ = None

    def load(self):
        if self.isLoaded():
            return self.data_
        generator = ArrayGenerator(**self.params_)
        array = generator.create(self.shape_,self.array_)
        offsets = [0] * len(self.slice_[0])
        for s in self.slice_:
            dests = [0] * len(s)
            for i in range(len(s)):
                ss = s[i]
                dests[i] = slice(offsets[i],ss.stop-ss.start + offsets[i],ss.step)
            array[dests] = self.array_[s]
            for i in range(len(s)):
                ss = s[i]
                if ss.stop - ss.start < array.shape[i]:
                    offsets[i] = ss.stop - ss.start
                else:
                    offsets[i] = 0
        return generator.postProcess(array,squeeze = True)

    def sqrt(self):
        return np.sqrt(self.load())
