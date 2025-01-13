import math

def float10Power(value):
    if value == 0:
        return 0
    d = math.log10(abs(value))
    if d >= 0:
        d = math.ceil(d)
    else:
        d = math.floor(d) - 1
    return d

def floatFormat(digits):
    d = abs(digits)
    if d <= 2:
        format = '.%df' % d
    else:
        format = '.1e'
    return '%' + format

def roundInteger(value):
    s = str(int(value))
    ll = len(s)
    if ll == 1:
        d = s[0]
        m = 0
    else:
        d = s[1]
        m = int(s[0])
    d = int(d)
    if d >= 5:
        m += 1
    trail = '0' * (len(s) - 1)
    if ll == 1 and m == 1:
        trail = '0'
    return int(str(m) + trail)

def bigNumber(value):
    s = str(value)
    l = s.split('.')
    whole = l[0]
    dec = ''
    if len(l) > 1:
        dec = l[1]
    new = ''
    ll = len(whole)
    for i in range(ll):
        indx = ll - i - 1
        new += whole[i]
        if indx % 3 == 0 and indx != 0:
            new += ','
    if len(dec) > 0:
        new += '.' + dec
    return new
