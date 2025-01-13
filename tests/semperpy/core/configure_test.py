import unittest
import os
import sys
from semperpy.core.configure import Configure

class ConfigureTest(unittest.TestCase):

    def setUp(self):    
        self.config_ = Configure('SEMPERPY')
        self.conf_ = '/semperpy/config'
        os.environ['SEMPERPY_CONFIG'] = self.conf_
        self.multi_conf_ = '/a/b:/c/d:/e/f'
        os.environ['SEMPERPY_MULTI'] = self.multi_conf_
        self.relative1_ = '~/tools'
        os.environ['SEMPERPY_RELATIVE1'] = self.relative1_
        self.relative2_ = '../tools'
        os.environ['SEMPERPY_RELATIVE2'] = self.relative2_
        self.pwd_ = os.getenv('PWD')
        self.pwd_conf_ = "/a/b:%s:~/b" % (self.pwd_)
        os.environ['SEMPERPY_PWD'] = self.pwd_conf_

    def test_path(self):
        self.assertEqual(self.config_.path('CONFIG'),[self.conf_])

    def test_subpath(self):
        self.assertEqual(self.config_.path('CONFIG','subdir'),[self.conf_ + '/subdir'])

    def test_relative_path1(self):
        self.assertEqual(self.config_.path('RELATIVE1'),[self.conf_ + '/tools'])

    def test_relative_path2(self):
        self.assertEqual(self.config_.path('RELATIVE2'),['../tools'])

    def test_multi_path(self):
        self.assertEqual(self.config_.path('MULTI'),self.multi_conf_.split(':'))

    def no_test_file(self):
        self.assertEqual(self.config_.file(sys.argv[0],'PWD'),[self.pwd_ + '/' + sys.argv[0]])

    def test_undefined(self):
        self.assertEqual(self.config_.path('TOTO'),['./'])

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ConfigureTest)
    unittest.TextTestRunner(verbosity=2).run(suite)


