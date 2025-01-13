#
# simpleArith.py
#
# Example of defining an arithmetic expression parser using
# the operatorPrecedence helper method in pyparsing.
#
# Copyright 2006, by Paul McGuire
#

from pyparsing import *

value = Word('-+0123456789').setParseAction(lambda t:float(t[0]))
variable = Word(alphas)
operand = value | variable
order = oneOf('== != <= < >= >')
combine = oneOf('and or')
operators = oneOf('+ - * /')

bioperators = set(['==','!=','<=','<','>=','>','and','or'])

expr = operatorPrecedence(operand,
    [
        (order, 2, opAssoc.LEFT),
        (combine, 2, opAssoc.LEFT),
    ]
)

class Node(object):
    def __init__(self,operator):
        self.left_ = None
        self.right_ = None
        self.operator_ = operator

    def left(self,what = None):
        if what != None:
            self.left_ = what
        return self.left_

    def right(self,what = None):
        if what != None:
            self.right_ = what
        return self.right_

    def value(self):
        return self.operator_

    def __str__(self,tab = '',ident='   '):
        return '%s%s\n%s%s%s%s' % (tab,self.value(),tab,self.left_.__str__(tab+ident),tab,self.right_.__str__(tab+ident))

class Leaf(object):

    def __init__(self,value):
        self.value_ = value

    def value(self):
        return self.value_

    def __str__(self,tab = None):
        return tab + str(self.value_) + '\n'
    

def build(x):
    if isinstance(x,ParseResults):
        nodes = []
        done = set()
        i = 1
        while i < len(x):
            v = x[i]
            if v in bioperators:
                node = Node(v)
                if not i-1 in done:
                    node.left(build(x[i-1]))
                else:
                    node.left(nodes[-1])
                if i+1 in done:
                    raise IndexError('something went wrong analysing the syntax')
                node.right(build(x[i+1]))
                done.add(i-1)
                done.add(i)
                done.add(i+1)
                nodes.append(node)
            i = i + 2
        return nodes[-1]
    else:
        return Leaf(x)


test = [
            "kx == 4",
            "kx == 4 and kt == 289",
            "lat < -20",
            "kx == 4 and kt == 289 and (lat < -20 or lat > 20)",
            "(kx == 4 or kx == 12) and kt == 289",
            "kx == 4 and obs < 12 and kx == kt"
       ]

for t in test:
    print(t)
    x = expr.parseString(t)
    print(x[0])
    node = build(x[0])
    print(node)
    print() 

