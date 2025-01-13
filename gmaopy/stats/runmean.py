from semperpy.slicing.arraygenerator import ArrayGenerator

class RunMean(object):

    def __init__(self,window):
        if window % 2 != 0:
            window -= 1
        self.window_ = window

    def __call__(self,data,values):
        array = ArrayGenerator(missing_value=1.7E38)

runmean = RunMean
