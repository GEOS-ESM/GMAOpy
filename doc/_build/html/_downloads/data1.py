from semperpy.directive.directive import Directive

class Data1(Directive):
    def __init__(self,*args,**kargs):
        super(Data1,self).__init__(*args,**kargs)
        self.checkLanguage()

d = Data1(
    domain_name = ['glob'],
    channel = [1,2,3,4,5],
    kt = 40,
    kx = [314,315,316,317,318,319,300,325],
    date = '2011010100'
)

print(d)
