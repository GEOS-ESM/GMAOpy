# Claude Gibert Aug 2011
import sys
import os
import os.path
import time
import glob
import shutil
from semperpy.core.tools import substitute_unix_dates
from semperpy.core.configfile import ConfigFile
from semperpy.core.date import Dates, Date
from gmaopy.retrieve.retriever import Retriever
from semperpy.archive.dmf.dmf import DMF

# we need the full path to where we copy all the obs files
if len(sys.argv) < 3:
    raise SystemError('expect a destination directory and an experiment / date file')
dest = sys.argv[1]
config = sys.argv[2]

# maximum number of dates to be staged and copied until consumed
max_ready = 10
# maximum number of dates to keep online once consumed
max_done = 5
name = os.path.basename(config).split('.')
progress_file = '%s/progress_%s.def' % (dest,name[0])

# we sort dictionaries using their start date, not extremely important but pretty
def mySort(a,b):
    return cmp(a['start'],b['start'])

# just counts the number of .ready directories because we don't want to exceed it
def count_ready_dates(path):
    path = path + '/' + '*.ready'
    files = glob.glob(path)
    return len(files)

# checks the number of .done directories (processed by the computing job)
# if reached, we delete the older ones
def check_done(path):
    path = path + '/' + '*.done'
    files = sorted(glob.glob(path))
    to_delete = len(files) - max_done
    print(to_delete,'<stager> files to be deleted')
    if to_delete > 0:
        for file in files[0:to_delete]:
            print('<stager> deleting',file)
            shutil.rmtree(file,ignore_errors = True)

prev_date = None
prev_expver = None
try:
    f = open(progress_file,'r')
    line = f.readline()[0:-1]
    prev_date,prev_expver = line.split(' ')
except IOError:
    pass

tree = 'Ydate(@Y)/Mdate(@m)'
config = ConfigFile(config)
segments = sorted(list(config.values()),mySort)
for segment in segments:
    step = segment.get('step',24)
    print(segment)
    print(int(segment['start']),int(segment['end']),int(step))
    for date in Dates(int(segment['start']),int(segment['end']),int(step)):
            expver = segment['expver']
            if prev_date is None or int(date) > int(prev_date):
                dir = '%s/%s.%s.stage' % (dest,str(date),expver)
                dst = '%s/%s.%s.copy' % (dest,str(date),expver)
                print(dir)
                if not os.path.exists(dir) and not os.path.exists(dst):
                    os.mkdir(dir)
                    location = segment['archive_location'] 
                    path = substitute_unix_dates(location + '/' + tree,'date',Date(date))
                    files = glob.glob(path + '/' + '%s.aod.obs*.ods' % expver)
                    print('<stager>',date,len(files),'files')
                    dmf = DMF(files)
                    dmf.stage()
                    print("<stager> staging done")
                    os.rename(dir,dst)
                    for file in files:
                        shutil.copy(file,dst)
                    final = '%s/%s.%s.ready' % (dest,str(date),expver)
                    os.rename(dst,final)
                    f = open(progress_file,'w')
                    f.write('%s %s\n' % (str(date),expver))
                    f.close()
                    check_done(dest)
                    ready = count_ready_dates(dest)
                    while ready >= max_ready:
                        ready = count_ready_dates(dest)
                        # sleep 1 minute to wait for the consumer to consume
                        time.sleep(60)
