import sys
import settings

which = sys.argv[1]
what = sys.argv[2]

if which == 'time':
    ref = list(settings.time.keys())
    if not what in ref:
        print('Unknown time frame: "%s", please specify amongst: "%s"' % (what,', '.join(ref)))
        exit(1)
elif which == 'scripts':
    ref = settings.scripts
    if not what in ref:
        print('Unknown script: "%s", please specify amongst: "%s"' % (what,', '.join(ref)))
        exit(1)
    if len(sys.argv) < 4:
        print('With keyword "scripts" the script option is expected')
        exit(1)
    option = sys.argv[3]
    if not option in list(ref[what].keys()):
        print('Unknown script option: "%s" for "%s", please specify amongst: "%s"' % (option,what,', '.join(list(ref[what]))))
        exit(1)
else:
    print('unknow group "%s"' % which)
