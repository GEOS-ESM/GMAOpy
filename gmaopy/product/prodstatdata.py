from gmaopy.stats.statdata import StatData
from gmaopy.score.scoretexttemplate import ScoreTextTemplate

class ProdStatData(StatData):
    def createTextTemplate(self):
        return ScoreTextTemplate()

    def prefixName(self):
        return 'SEMPERPY','prodtitles.def'

prodstatdata = ProdStatData
