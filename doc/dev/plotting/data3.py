import os
from semperpy.directive.directive import Directive

class Data(Directive):

    def __init__(self,*args,**kargs):
        super(Data,self).__init__(*args,**kargs)
        self.checkLanguage()

class Attributes(Directive):
    pass


d = Data(
    level = ['1000','500'],
    domain_name = 'global',
    channel = [1,2,3,4,5],
    kt = 4,
    kx = 220,
    date = '2011010100'
)

print(d)
