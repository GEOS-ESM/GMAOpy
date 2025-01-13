from semperpy.core.tools import nocasedict
from semperpy.core.configure import Configure
from semperpy.core.configfile import ConfigFile

class Parameter(object):

    kt_to_shortname_ = {}
    shortname_to_kt_ = {}

    @classmethod
    def read(self):
        if len(self.kt_to_shortname_) == 0:
            configure = Configure('semperpy')
            files = configure.file('parameter.def','CONFIG','ods')
            config = ConfigFile(files)
            for kt,p in config.items():
                kt = int(kt)
                self.kt_to_shortname_[kt] = dict(p)
                self.shortname_to_kt_[p['shortname']] = kt

    @classmethod
    def shortname(self,kt):
        self.read()
        return self.kt_to_shortname_[kt]['shortname']

    @classmethod
    def unit(self,kt):
        self.read()
        return self.kt_to_shortname_[kt]['unit']

    @classmethod
    def title(self,kt):
        self.read()
        return self.kt_to_shortname_[kt]['title']

    @classmethod
    def kt(self,shortname):
        self.read()
        return self.shortname_to_kt_[shortname]

    @classmethod
    def free(self):
        self.kt_to_shortname_ = None
        self.shortname_to_kt_ = None
