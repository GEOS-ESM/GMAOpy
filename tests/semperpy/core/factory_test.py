import unittest
from semperpy.core.factory import Factory, SingletonFactory
#----------------------------------------------------------------------------
# VeryPy Copyright SynopticView 2009-2010
# http://www.synopticview.com
#
# Claude Gibert, December 2009
#----------------------------------------------------------------------------

class FactoryTest(unittest.TestCase):

    def test_functions(self):
        def hello(what):
            if what == 'world':
                return True
            return False

        f = Factory()
        f.register('hello',hello)
        self.assertTrue(f.create('hello','world'))

    def test_classes(self):
        class Hello(object):
            def __init__(self,what):
                self.what = what
            def __call__(self):
                if self.what == 'cworld':
                    return True
                return False
        f = Factory()
        f.register('chello',Hello)
        self.assertTrue(f.create('chello','cworld')())

    def test_duplicates(self):
        def hello():
            pass
        f = Factory()
        f.register('dummy',hello)
        with self.assertRaises(IndexError):
            f.register('dummy',hello)

        f = Factory(noduplicates=False)
        f.register('dummy',hello)
        f.register('dummy',hello)

    def test_default(self):
        def hello():
            pass
        f = Factory()
        with self.assertRaises(IndexError):
            f.create('dummy','world')
        f.register('default',hello)
        with self.assertRaises(IndexError):
            f.create('dummy','world')
        f = Factory(hasdefault=False)
        with self.assertRaises(IndexError):
            f.create('dummy','world')

    def test_singleton(self):
        class Hello(object):
            pass
        f = SingletonFactory()
        f.register('Hello',Hello)
        o = f.create('Hello')
        p = f.create('Hello')
        self.assertEqual(id(o),id(p))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(FactoryTest)
    unittest.TextTestRunner(verbosity=2).run(suite)


