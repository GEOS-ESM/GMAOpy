addx = 1 
def genadd(x) : 
    global addx 
    addx += x 
    def addy(y) : 
        return addx + y 
    return addy

f = genadd(4)
print(f(5))
f = genadd(4)
print(f(5))
