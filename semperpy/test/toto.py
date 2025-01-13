def combinations(keywords,values,current = []):
    result = []
    if len(keywords) > 0:
        keyword = keywords[0]
        for value in values[keyword]:
            result.append(combinations(keywords[1:],values,current + [value]))
    else:
        return current
    return result
            
            
values = dict(
    steps = [12,24],
    parameters = ['u','v'],
    dates = [20110101,20110102]
)

v = combinations(['dates','parameters','steps'],values)
for vv in v:
    print(vv)
print()
v = combinations(['parameters','dates','steps'],values)
for vv in v:
    print(vv)
print()
v = combinations(['steps','parameters','dates'],values)
for vv in v:
    print(vv)
print()
