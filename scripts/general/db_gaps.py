import sys
from semperpy.core.date import Date
from gmaopy.db.database import Database

if len(sys.argv) < 2:
    raise RuntimeError('database name is expected')

database = sys.argv[1]

db = Database(database,write=False)
result = db.query('select distinct date from %s.v_view order by date;' % database)
previous = Date(result[0][0])
intervals = []
for row in result[1:]:
    date = Date(row[0])
    diff = date - previous 
    intervals.append(diff)
    print(diff,date,previous)
    previous = date
