from semperpy.directive.directive import Directive
from semperpy.plot.mplib.graphdirective import GraphDirective

class Attribute(GraphDirective):

    def __getattr__(self,attr):
        # this is a syntax sweetening trick, any method can be called
        # on that object:
        # self.attribute(value)  <=> self[attribute] = value
        # print self.attribute() <=> print self[attribute]
        class Assign(object):

            def __init__(self,attr,host):
                self.attr_ = attr
                self.host_ = host

            def __call__(self,value = None):
                if not value is None:
                    self.host_[self.attr_] = value
                return self.host_[self.attr_]

        return Assign(attr,self)
