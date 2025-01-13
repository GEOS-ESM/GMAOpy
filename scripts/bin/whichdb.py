import sys
from semperpy.core.configure import Configure
from semperpy.core.configfile import ConfigFile

database = sys.argv[1]

configure = Configure('semperpy')
loc = configure.localise()
databases = ConfigFile(configure.file('databases%s.def' % loc,'CONFIG','db'))
database = databases[database]
print(database['database'])
print(database['userw'])
