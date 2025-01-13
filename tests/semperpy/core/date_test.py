import unittest
from semperpy.core import *
#----------------------------------------------------------------------------
# VeryPy Copyright SynopticView 2009-2010-2011
# http://www.synopticview.com
#
# Claude Gibert, December 2009
#----------------------------------------------------------------------------
years = {
            'value': 2009,
            '+'    : [[2015,6],[2027,18],[2008,-1],[1994,-15]],
            '-'    : [[2015,-6],[2027,-18],[2008,1],[1994,15]],
            'sub'  : [[2015,-6],[2027,-18],[2008,1],[1994,15]],
            '=='   : [[2009,True],[Year(2009),True],[2008,False],[Date(2008),False]],
            '<='   : [[2009,True],[Year(2009),True],[2010,True],[Date(2010),True]],
            '>='   : [[2009,True],[Year(2009),True],[2010,False],[Date(2010),False]],
            '<'    : [[2009,False],[Year(2009),False],[2010,True],[Date(2010),True]],
            '>'    : [[2009,False],[Year(2009),False],[2010,False],[Date(2010),False]],
}

months = {
            'value': 200902,
            '+'    : [[200908,6],[201008,18],[200901,-1],[200711,-15]],
            '-'    : [[200908,-6],[201008,-18],[200901,1],[200711,15]],
            'sub'  : [[200908,-6],[201008,-18],[200901,1],[200711,15]],
            '=='   : [[200902,True],[Month(200902),True],[200906,False],[Date(200906),False]],
            '<='    : [[200902,True],[Month(200902),True],[200906,True],[Date(200906),True]],
            '>='    : [[200902,True],[Month(200902),True],[200906,False],[Date(200906),False]],
            '<'    : [[200902,False],[Month(200902),False],[200906,True],[Date(200906),True]],
            '>'    : [[200902,False],[Month(200902),False],[200906,False],[Date(200906),False]],
}

days = {
            'value': 20090211,
            '+'    : [[20090217,6],[20090301,18],[20090210,-1],[20090127,-15]],
            '-'    : [[20090217,-6],[20090301,-18],[20090210,1],[20090127,15]],
            'sub'  : [[20090217,-6],[20090301,-18],[20090210,1],[20090127,15]],
            '=='   : [[20090211,True],[Day(20090211),True],[20090604,False],[Date(20090604),False]],
            '<='   : [[20090211,True],[Day(20090211),True],[20090604,True],[Date(20090604),True]],
            '>='   : [[20090211,True],[Day(20090211),True],[20090604,False],[Date(20090604),False]],
            '<'   : [[20090211,False],[Day(20090211),False],[20090604,True],[Date(20090604),True]],
            '>'   : [[20090211,False],[Day(20090211),False],[20090604,False],[Date(20090604),False]],
}

hours = {
            'value': 2009021112,
            '+'    : [[2009021200,12],[2009022512,336],[2009021111,-1],[2009021021,-15]],
            '-'    : [[2009021200,-12],[2009022512,-336],[2009021111,1],[2009021021,15]],
            'sub'  : [[2009021200,-12],[2009022512,-336],[2009021111,1],[2009021021,15]],
            '=='   : [[2009021112,True],[Hour(2009021112),True],[2009060423,False],[Date(2009060423),False]],
            '<='   : [[2009021112,True],[Hour(2009021112),True],[2009060423,True],[Date(2009060423),True]],
            '>='   : [[2009021112,True],[Hour(2009021112),True],[2009060423,False],[Date(2009060423),False]],
            '<'   : [[2009021112,False],[Hour(2009021112),False],[2009060423,True],[Date(2009060423),True]],
            '>'   : [[2009021112,False],[Hour(2009021112),False],[2009060423,False],[Date(2009060423),False]],
}

minutes = {
            'value': 200902111230,
            '+'    : [[200902111242,12],[200902111806,336],[200902111229,-1],[200902101230,-1440]],
            '-'    : [[200902111242,-12],[200902111806,-336],[200902111229,1],[200902101230,1440]],
            'sub'  : [[200902111242,-12],[200902111806,-336],[200902111229,1],[200902101230,1440]],
            '=='   : [[200902111230,True],[Minute(200902111230),True],[200902111231,False],[Date(200902111231),False]],
            '<='   : [[200902111230,True],[Minute(200902111230),True],[200902111231,True],[Date(200902111231),True]],
            '>='   : [[200902111230,True],[Minute(200902111230),True],[200902111231,False],[Date(2009060421),False]],
            '<'   : [[200902111230,False],[Minute(200902111230),False],[200902111231,True],[Date(200902111231),True]],
            '>'   : [[200902111230,False],[Minute(200902111230),False],[200902111231,False],[Date(200902111231),False]],
}

seconds = {
            'value': 20090211123045,
            '+'    : [[20090211123105,20],[20090211123245,120],[20090211123000,-45],[20090211113309,-3456]],
            '-'    : [[20090211123105,-20],[20090211123245,-120],[20090211123000,45],[20090211113309,3456]],
            'sub'  : [[20090211123105,-20],[20090211123245,-120],[20090211123000,45],[20090211113309,3456]],
            '=='   : [[20090211123045,True],[Second(20090211123045),True],[20090211123046,False],[Date(20090211123046),False]],
            '<='   : [[20090211123045,True],[Second(20090211123045),True],[20090211123046,True],[Date(20090211123046),True]],
            '>='   : [[20090211123045,True],[Second(20090211123045),True],[20090211123046,False],[Date(20090211123046),False]],
            '<'   : [[20090211123045,False],[Second(20090211123045),False],[20090211123046,True],[Date(20090211123046),True]],
            '>'   : [[20090211123045,False],[Second(20090211123045),False],[20090211123046,False],[Date(20090211123046),False]],
}

class DateTest(unittest.TestCase):

    entries_ = [years,months,days,hours,minutes,seconds]

    def test_arithemtic(self):
        for op in ['+','-']:
            for entry in self.entries_:
                for t in entry[op]:
                    d = Date(entry['value'])
                    action = op + ' ' + str(t[1])
                    r = eval('d ' + action)
                    self.assertEqual(t[0],r.intvalue())
        for op in ['sub']:
            for entry in self.entries_:
                for t in entry[op]:
                    d = Date(entry['value'])
                    action = ' -  Date(' + str(t[0]) + ')'
                    r = eval('d ' + action)
                    self.assertEqual(t[1],r)

    def test_logical(self):
        for op in ['==','<=','>=','<','>']:
            for entry in self.entries_:
                for t in entry[op]:
                    d = Date(entry['value'])
                    if isinstance(t[0],int):
                        second = str(t[0])
                        action = op + ' ' + second
                        what =  action
                    else:
                        second = t[0]
                        action = op + ' second'
                        what  = op + ' ' + second.__str__()
                    r = eval('d ' + action)
                    self.assertEqual(r,t[1])

    def test_increment(self):

        a1 = [20090201,20090202,20090203,20090204,20090612,20090614,20090616]
        a2 = [2009021106,2009021112,2009021118,2009021200,2009021206]
        a3 = [2009021106,2009021112,2009021118,2009021200,2009021206,2009022000,2009021912,2009021900,2009021812]
        a4 = [20091215,20100115,20100215]
        a5 = [2009121500,2010011601,2010021702,2010031803]
        a6 = [2009121500,2010011612,2010021800,2010031912,2010042100]
        a7 = [20021118124500,20031219134601,20050120144702]

        self.assertEqual(a1,Dates(20090201,20090204,1,20090612,20090616,2))
        self.assertEqual(a2,Dates(2009021106,2009021206,6))
        self.assertEqual(a3,Dates(2009021106,2009021206,6,2009022000,2009021812,-12))
        self.assertEqual(a4,Dates(20091215,20100215,DateIncrement(months=1)))
        self.assertEqual(a5,Dates(2009121500,2010031803,DateIncrement(months=1,days=1,hours=1)))
        self.assertEqual(a6,Dates(2009121500,2010042100,DateIncrement(months=1,days=1,hours=12)))
        self.assertEqual(a7,Dates(20021118124500,20050120144702,DateIncrement(years=1,months=1,days=1,hours=1,minutes=1,seconds=1)))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DateTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
