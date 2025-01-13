import math

class Turtle(object):

    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.angle = 0

    def forward(self,distance):
        self.x += distance * math.cos(self.angle)
        self.y += distance * math.sin(self.angle)

    def left(self,angle):
        self.angle += angle / 180.0 * math.pi

    def right(self,angle):
        self.angle -= angle / 180.0 * math.pi

    def __str__(self):
        return "x = %f y = %f" % (self.x,self.y)

    def __iadd__(self,value):
        self.forward(value)
        return self

    def __imul__(self,value):
        self.left(value)
        return self

    def __idiv__(self,value):
        self.right(value)
        return self
        
t = Turtle() # no need for arguments
t += 10
print(t)
t *= 45
t += 10
print(t)
t /= 45
t += -12
print(t)
