import numpy

class MyOwnArray(object):

    def __init__(self,array):
        self.array = array

    def __getattr__(self,attribute):
        return getattr(self.array,attribute)

    def __str__(self):
        return self.array.__str__()

    def __add__(self,value):
        return self.array.__add__(value)

array = numpy.arange(12)
print(array)
a = MyOwnArray(array)
print(a.shape)
print(a.mean())
print(a)
print(a + 12)
