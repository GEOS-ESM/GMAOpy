import copy
import numpy.ma as ma
from semperpy.core.tools import nestedLoops
from semperpy.core.index import Index
from semperpy.slicing.arraygenerator import ArrayGenerator
from gmaopy.storage.reader import Reader
from gmaopy.stats.statdata import StatData
from gmaopy.score.scoretexttemplate import ScoreTextTemplate

class ScoreData(StatData):

    def createTextTemplate(self):
        return ScoreTextTemplate()

    def prefixName(self):
        return 'SEMPERPY','scoretitles.def'

    def category(self):
        return 'score'

scoredata = ScoreData
