import unittest
import numpy as np
from semperpy.slicing.cf10.leveldimension import LevelDimension

class LevelDimensionTest(unittest.TestCase):

    name        = 'dim'
    official    = 'official'
    variable    =  np.array([1000,975,950,925,900,875,850,825,800,750,700,650,600,550,500,450, 400, 350, 300, 250, 200, 150, 100, 70, 50, 40, 30, 20, 10, 7,5,3, 2, 1, 0.400000005960464, 0.200000002980232])

    def setUp(self):
        self.dim_ = LevelDimension(self.name,self.official,self.variable)

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
        self.assertEqual(list(lim),[1000,0.200000002980232])

    def test_contains(self):
        values = [975,972,2500]
        results = [True,True,False]
        for i in range(len(values)):
            self.assertEqual(values[i] in self.dim_, results[i])

    def test_slicing(self):
        s = self.dim_.findSlice([500,100])
        self.assertEqual(s,[slice(14, 15, 1), slice(22, 23, 1)])
        s = self.dim_.findSlice({970:250})
        self.assertEqual(s,[slice(1, 20, 1)])
        s = self.dim_.findSlice({675:8})
        self.assertEqual(s,[slice(10, 30, 1)])
        with self.assertRaises(IndexError):
            s = self.dim_.findSlice([1000,500,250,2000])

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(LevelDimensionTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
