
class Drawer(object):

    def __init__(self,klass):
        self.class_ = klass

    def graphicalObject(self):
        return self.class_()

    def calculateMinMax(self,datacollection):
        minv = None
        maxv = None
        for data in datacollection:
            values = data.value
            for v in values:
                if v != data.missingValue():
                    if minv is None or v < minv:
                        minv = v
                    if maxv is None or v > maxv:
                        maxv = v
#        print('IN DRAWER', minv)
        allmissing = minv is None
        return minv,maxv,allmissing
