from gmaopy.stats.statdata import StatData
from gmaopy.score.scoretexttemplate import ScoreTextTemplate

class ProdData(StatData):

    def category(self):
        return 'product'

    def createTextTemplate(self):
        return ScoreTextTemplate()

    def prefixName(self):
        return 'SEMPERPY','prodtitles.def'

proddata = ProdData
