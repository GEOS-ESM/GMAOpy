from semperpy.core.tools import to_list
from gmaopy.stats.statdata import StatData
from gmaopy.ods.odsinfo import ODSInfo
from gmaopy.stats.statistics import Statistics
from gmaopy.obs.obstexttemplate import ObsTextTemplate

class ObsPlotData(StatData):

    def missingValue(self):
        return Statistics.missing_value

    def assignLevels(self,data):
        replace = False
        for one in data:
            if 'kx' in one and 'kt' in one:
                #if 'level' in one and to_list(one['level'])[0] == 'all' or not 'level' in one:
                if 'level' in one and to_list(one['level'])[0] == 'all':
                    level,levtype = self.findLevels(one)
                    if len(level) > 0:
                        one['level'] = level
                    else:
                        del(one['level'])
                    if len(levtype) > 0:
                        one['levtype'] = levtype
                    elif 'levtype' in one:
                        del(one['levtype'])
                else:
                    dummy1,dummy2 = self.findLevels(one,enforced=False)
                    if dummy2 is not None:
                        one['levtype'] = dummy2

    def findLevels(self,data,enforced = True):
        kxs = to_list(data['kx'])
        kts = to_list(data['kt'])
        info = ODSInfo()
        all = []
        lev = set()
        typ = set()
        for kx in kxs:
            for kt in kts:
                # in some cases when many instruments are mixed, we end up
                # with a mixture of level types, in that case we just
                # don't need the information and ignore the error.
                try:
                    levtype,levels = info.levelsOf(kx,kt)
                    all.append(levels)
                    lev.add(levels)
                    typ.add(levtype)
                except:
                    pass
        if enforced:
            if len(typ) > 1 or len(lev) > 1:
                raise ValueError('cannot mix different types of levels or different levels')
        else:
            typ = list(typ)
            if len(typ) > 1:
                typ = None
            else:
                typ = typ[0]
            return [],typ
        if len(all) == 0:
            all = [[]]
        levtype = list(typ)
        if len(levtype) == 0:
            levtype = [[]]
        return all[0],levtype[0]

    def createTextTemplate(self):
        return ObsTextTemplate()
