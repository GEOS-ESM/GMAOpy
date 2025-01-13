import unittest
import numpy as np
from semperpy.core.date import Hour
from semperpy.slicing.cf10.datedimension import DateDimension

class DateDimensionTest(unittest.TestCase):
    name = 'time'
    official = 'date'

    class ArrayProxy(np.ndarray):
        pass

    class Meta(object):
        def __call__(self,dimension,name):
            return getattr(dimension.variable_,name)

    def setUp(self):
        values = [0,360,720,1080]
        self.variable_ = self.ArrayProxy(len(values),np.float64)
        self.variable_[:] = values[:]
        self.variable_.units = "minutes since 2010-03-10 18:00:00"
        self.dim_ = DateDimension(self.name,self.official,self.variable_,self.Meta())
        self.dates_ = [Hour(2010031018),Hour(2010031100),Hour(2010031106),Hour(2010031112)]

    def test_accessors(self):
        self.assertEqual(self.dim_.name(),self.name)
        self.assertEqual(self.dim_.officialName(),self.official)

    def test_slicedimension(self):
        w = self.dates_[1:3]
        v = self.dim_.slice(slice(1,3,1))
        for i in range(len(w)):
            self.assertEqual(w[i],v[i])

    def test_cache(self):
        v = self.dim_.slice(slice(1,3,1))
        x = self.dim_.cache_[self.dim_.hash_slice(slice(1,3,1))]
        self.assertEqual(v,x)

    def test_limits(self):
        lim = self.dim_.limits()
        self.assertEqual(list(lim),[self.dates_[0],self.dates_[-1]])

    def test_contains(self):
        dates = [Hour(2010031018),Hour(2010031100),Hour(2010031106),Hour(2010031112)]
        values = [2010031018,2010031100,2010031118,2010031106]
        results = [True,True,False,True]
        for i in range(len(values)):
            self.assertEqual(values[i] in self.dim_, results[i])

    def test_slicing(self):
        s = self.dim_.findSlice([2010031018,2010031112])
        self.assertEqual(s,[slice(0, 1, 1), slice(3, 4, 1)])
        s = self.dim_.findSlice({2010031018:2010031112})
        self.assertEqual(s,[slice(0, 4, 1)])
        s = self.dim_.findSlice({2010031100:2010031109})
        self.assertEqual(s,[slice(1, 4, 1)])
        with self.assertRaises(IndexError):
            s = self.dim_.findSlice([2010031018,2010031100,2010031118,2010031106])

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DateDimensionTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
