import numpy as np
from semperpy.fields.containers.container import Container

class ArrayContainer(Container):
    def __init__(self,array):
        self.array_ = array

    def __call__(self):
        return self.array_

    def shape(self):
        return self.array_.shape

    def sqrt(self):
        return np.sqrt(self.array_)
