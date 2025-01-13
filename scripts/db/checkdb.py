import numpy as np
from semperpy.core.date import Dates, Date
from dbquery import DBQuery

q = DBQuery('ob_ops')

current = Date(201008)
while current.intvalue() < 201209:
    for cycle in (0,6,12,18):
        all = []
        begin = current.intvalue() * 10000 + 100 + cycle
        end = (current + 1).intvalue() * 10000 + 100 + cycle
        end = (Date(end) - 24).intvalue()
        dates = Dates(begin,end,24)
        print('%s, %02dZ' % (current,cycle))
        for date in dates:
            value = q('count(value)',dict(
                date = date,
            ))
            all.append(value[0][0])
        counts = np.zeros((len(all)))
        for i in range(len(all)):
            counts[i] = all[i]
        not_zero = counts != 0
        not_zero = counts[not_zero]
        std = np.std(not_zero)
        mean = np.mean(not_zero)
        done = False
        for i in range(len(all)):
            if counts[i] == 0 or abs(counts[i] - mean) > 3*std:
                print(dates[i],counts[i],mean,std)
                done = True
        if not done:
            print('ok')
        print()

    current += 1
    print()
