import unittest
import numpy as np
from semperpy.core.tools import ErrorCreator
from semperpy.slicing.dimensions.sorteddescending import SortedDescendingDimension
from .dimension_test import DimensionTest

class SortedDescendingTest(DimensionTest):

    name        = 'dim'
    official    = 'official'
    variable    = np.array([20,19,18,17,16,15,14,13,12])

    def setUp(self):
        self.dim_ = SortedDescendingDimension(self.name,self.official,self.variable)

    def test_accessors(self):
        self.assertEqual(self.dim_.name(),self.name)
        self.assertEqual(self.dim_.officialName(),self.official)

    def test_slicedimension(self):
        w = self.variable[1:4]
        v = self.dim_.slice(slice(1,4,1))
        x = v == w
        self.assertTrue(x.all())

    def test_cache(self):
        v = self.dim_.slice(slice(1,4,1))
        x = self.dim_.cache_[self.dim_.hash_slice(slice(1,4,1))]
        self.assertEqual(v,x)

    def test_limits(self):
        lim = self.dim_.limits()
        self.assertEqual(list(lim),[20,12])

    def test_contains(self):
        values = [12,18,25,15,[13,14,15],[14,45,56],{13:19},{13:25}]
        results = [True,True,False,True,True,False,True,False]
        for i in range(len(values)):
            self.assertEqual(values[i] in self.dim_, results[i])

    def test_slicing(self):
        s = self.dim_.findSlice([12,20])
        self.assertEqual(s,[slice(8, 9, 1), slice(0, 1, 1)])
        s = self.dim_.findSlice({17:13})
        self.assertEqual(s,[slice(3, 8, 1)])
        s = self.dim_.findSlice({20:12})
        self.assertEqual(s,[slice(0, 9, 1)])
        with self.assertRaises(IndexError):
            s = self.dim_.findSlice([12,15,25,20])

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SortedDescendingTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
