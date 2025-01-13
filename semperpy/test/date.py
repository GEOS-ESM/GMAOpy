from core import *
from datetime import *

d = Date(20091203)
print(d,type(d))
dd = Date(datetime(2009,12,0o3,14,42,45))
print(dd,type(dd))
m = Month(200303)
print(m,type(m))
print(Month(datetime(2009,12,0o3)))

print(dd.year())
print(dd.month())
print(dd.day())
print(dd.hour())
print(dd.minute())
print(dd.second())



d=Date(20090115)
one=DateIncrement(months=1)
