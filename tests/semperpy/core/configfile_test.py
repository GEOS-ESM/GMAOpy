import os
import unittest
from semperpy.core.configfile import ConfigFile

class ConfigFileTest(unittest.TestCase):

    def setUp(self):    
        config = """
[names]
name = verypy
int = 12
wrappedint = 14
list = 1,2,3,verypy,4
nested = [nested]

[nested]
a = 1
b = a
c = 1a

[__types__]
int=int
wrappedint = IntWrapper.IntWrapper
a = int
        """

        configfile = 'config.def'
        file = open(configfile,'w')
        file.write(config)
        file.close()

        intwrapper="""
class IntWrapper(object):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return str(self.value)
        """

        module = 'IntWrapper.py'
        file = open(module,'w')
        file.write(intwrapper)
        file.close()

    def tearDown(self):
        try:
            os.unlink('config.def')
            os.unlink('IntWrapper.py')
            os.unlink('IntWrapper.pyc')
            os.unlink('IntWrapper.pyo')
        except OSError:
            pass

    def test_values(self):
        config = ConfigFile('config.def')
        self.assertEqual(config['names']['name'],'verypy')
        self.assertEqual(config['names']['int'],12)
        self.assertEqual(config['names']['wrappedint'].__str__(), '14')
        self.assertEqual(config['names']['list'],['1','2','3','verypy','4'])
        self.assertEqual(config['names']['nested']['a'],1)
        self.assertEqual(config['names']['nested']['b'],'a')
        self.assertEqual(config['names']['nested']['c'],'1a')

    
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ConfigFileTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
