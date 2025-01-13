import unittest
import numpy as np
from semperpy.slicing.cf10.latdimension import LatDimension

class LatDimensionTest(unittest.TestCase):

    name        = 'dim'
    official    = 'official'
    variable    =  np.array([-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10])


    def setUp(self):
        self.dim_ = LatDimension(self.name,self.official,self.variable)

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
        self.assertEqual(list(lim),[-10,10])

    def test_contains(self):
        values = [5,-1,-9,10,[4,5,6],[14,45,56],{8:19},{-1:3}]
        results = [True,True,True,True,True,False,False,True]
        for i in range(len(values)):
            self.assertEqual(values[i] in self.dim_, results[i])

    def test_slicing(self):
        s = self.dim_.findSlice([-1,0.76])
        self.assertEqual(s,[slice(9, 10, 1), slice(11, 12, 1)])
        s = self.dim_.findSlice({-5.2:1.2})
        self.assertEqual(s,[slice(4, 13, 1)])
        s = self.dim_.findSlice([-9.8,9.2,-0.7,1.6])
        self.assertEqual(s,[slice(0, 1, 1), slice(19, 20, 1), slice(9, 10, 1), slice(12, 13, 1)])
        with self.assertRaises(IndexError):
            s = self.dim_.findSlice([-9.8,-50])

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(LatDimensionTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
