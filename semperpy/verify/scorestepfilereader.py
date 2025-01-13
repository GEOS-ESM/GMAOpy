import numpy as np
from semperpy.core.tools import to_list
from semperpy.verify.scorefilereader import ScoreFileReader

class ScoreStepFileReader(ScoreFileReader):

    def __init__(self,*args,**kargs):
        super(ScoreStepFileReader,self).__init__(*args,**kargs)
        self.read()
        print(self.scores_)

    def __call__(self,**kargs):
        kargs = dict(kargs)
        if 'step' in kargs:
            steps = to_list(kargs['step'])
            dates = to_list(kargs['date'])
            result = {}
            for date in dates:
                entry = []
                kargs['date'] = date
                for step in steps:
                    kargs['step'] = step
                    entry.append(self.scores_.constrained_access(**kargs))
                result[date] = np.array(entry)
        return result

