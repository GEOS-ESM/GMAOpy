import unittest
import numpy as np
from semperpy.slicing.slicer import Slicer
from semperpy.slicing.slice2array import Slice2Array
from semperpy.slicing.dimensions.dimension import Dimension
from semperpy.slicing.dimensions.indexed import IndexedDimension
from semperpy.slicing.dimensions.sortedascending import SortedAscendingDimension

class SlicerTest(unittest.TestCase):

    def setUp(self):
        v1 = [3,4,5,20]
        v2 = [6,8,10,12]
        dimensions = []
        dimensions.append(SortedAscendingDimension('dim1','dimension1',v1))
        dimensions.append(IndexedDimension('dim2','dimension2',v2))
        self.slicer_ = Slicer(dimensions)

    def test_slices(self):
        variable = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])
        directive = dict(
            dimension1 = {4:20},
            dimension2 = {8:12}
        )
        s = Slice2Array()
        self.slicer_(variable,directive,s)
        v = s.array()
        same = v == variable[1:4,1:4]
        self.assertTrue(same.all())
        directive = dict(
            dimension1 = {4:20},
            dimension2 = [8,12]
        )
        s = Slice2Array()
        self.slicer_(variable,directive,s)
        v = s.array()
        same = v == variable[1:4,[1,3]]
        self.assertTrue(same.all())
        directive = dict(
            dimension2 = {6:10}
        )
        s = Slice2Array()
        self.slicer_(variable,directive,s)
        v = s.array()
        same = v == variable[0:4,0:3]
        self.assertTrue(same.all())
   
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SlicerTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
