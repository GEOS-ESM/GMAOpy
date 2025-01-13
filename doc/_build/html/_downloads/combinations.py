def combinations(keywords,values,result,current = []):
    if len(keywords) > 0:
        keyword = keywords[0]
        for value in values[keyword]:
            combinations(keywords[1:],values,result,current + [value])
    else:
        result.append(current)
            
values = dict(
    steps = [12,24],
    parameters = ['u','v'],
    dates = [20110101,20110102]
)
a  = []
combinations(['dates','parameters','steps'],values,a)
for v in a:
    print(v)
print()
b = []
combinations(['parameters','dates','steps'],values,b)
for v in b:
    print(v)
print()
c = []
v = combinations(['steps','parameters','dates'],values,c)
for v in c:
    print(v)
print()
