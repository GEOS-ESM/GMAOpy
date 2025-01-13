import types
from pyparsing import *

class TruthParser(object):

    numbers         =   '-+0123456789'
    comparison      =   ['==','!=','<=','<','>=','>']
    logical         =   ['and','or']
    comparisonSet   =   set(comparison)
    logicalSet      =   set(logical)
    bioperators     =   set(comparison + logical)
        
    class Root(object):
        def __str__(self):
            return str(self.value_)

    class Comparison(Root):
        map = {
            '<':    '__lt__',
            '>':    '__gt__',
            '<=':   '__le__',
            '>=':   '__ge__',
            '==':   '__eq__',
            '!=':   '__ne__',
        }

        def __init__(self,what,*args,**kargs):
            self.value_  = what

        def __call__(self,a,b):
            a = a()
            b = b()
            f = getattr(a,self.map[self.value_])
            return f(b)

    class Logical(Root):
        
        def __init__(self,what):
            self.value_ = what
        
        def __call__(self,a,b):
            if self.value_ == 'and':
                return a and b
            else:
                return a or b

    class Value(Root):

        def __init__(self,value):
            self.value_ = value

        def __call__(self):
            return self.value_

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

    def __init__(self):
        value = Word(self.numbers).setParseAction(lambda t:float(t[0]))
        variable = Word(alphas)
        operand = value | variable
        order = oneOf(' '.join(self.comparison))
        combine = oneOf(' '.join(self.logical))
        self.expression_ = operatorPrecedence(operand,
                            [
                                (order, 2, opAssoc.LEFT),
                                (combine, 2, opAssoc.LEFT),
                            ]
                        )

    def parse(self,what,creator):
        x = self.expression_.parseString(what)
        self.tree_ = self.build(x[0],creator)
        return self.execute(self.tree_)

    def creatorMethod(self,creator,name):
        try:
            m = getattr(creator,name)
        except AttributeError:
            m = getattr(self,name)
        return m

    def build(self,x,creator):
        if isinstance(x,ParseResults):
            nodes = []
            done = set()
            i = 1
            while i < len(x):
                v = x[i]
                if v in self.bioperators:
                    if v in self.comparisonSet:
                        nodeInstance = self.creatorMethod(creator,'createComparison')
                    else:
                        nodeInstance = self.creatorMethod(creator,'createLogical')
                    node = self.Node(nodeInstance(v))
                    if not i-1 in done:
                        node.left(self.build(x[i-1],creator))
                    else:
                        node.left(nodes[-1])
                    if i+1 in done:
                        raise IndexError('something went wrong analysing the syntax')
                    node.right(self.build(x[i+1],creator))
                    done.add(i-1)
                    done.add(i)
                    done.add(i+1)
                    nodes.append(node)
                i = i + 2
            return nodes[-1]
        else:
            if type(x) == float:
                nodeInstance = self.creatorMethod(creator,'createValue')
            else:
                nodeInstance = self.creatorMethod(creator,'createVariable')
            return self.Leaf(nodeInstance(x))

    def execute(self,tree):
        if isinstance(tree,self.Node):
            left = self.execute(tree.left())
            right = self.execute(tree.right())
            op = tree.value()
            return op(left,right)
        else:
            return tree.value()

    def createLogical(self,what):
        return self.Logical(what)

    def createComparison(self,what):
        return self.Comparison(what)

    def createVariable(self,what):
        return self.Variable(what,self.file_)

    def createValue(self,what):
        return self.Value(what)
