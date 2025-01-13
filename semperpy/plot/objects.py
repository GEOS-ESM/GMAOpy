from semperpy.plot.curve import Curve

def line(*args,**kargs):
    kargs['kind'] = 'line'
    return Curve(*args,**kargs)

def bar(*args,**kargs):
    kargs['kind'] = 'bar'
    return Curve(*args,**kargs)

def dot(*args,**kargs):
    kargs['kind'] = 'dot'
    return Curve(*args,**kargs)

def stackedbar(*args,**kargs):
    kargs['kind'] = 'stackedbar'
    return Curve(*args,**kargs)

def shiftedbar(*args,**kargs):
    kargs['kind'] = 'shiftedbar'
    return Curve(*args,**kargs)

def splitbar(*args,**kargs):
    kargs['kind'] = 'splitbar'
    return Curve(*args,**kargs)
