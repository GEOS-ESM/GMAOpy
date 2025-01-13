from semperpy.core.configfile import ConfigFile
from semperpy.core.configure import Configure
from semperpy.language.validate import languageValidation

class Domain(object):

    domains_ = {}

    def __init__(self,north=90.0,west=-180.0,south=-90.0,east=180.0):
        self.north_ = north
        self.west_  = west
        self.south_ = south
        self.east_  = east

    def coordinates_ns(self):
        return self.north_,self.west_,self.south_,self.east_

    def coordinates_sn(self):
        return self.south_,self.west_,self.north_,self.east_

    def coordinates(self):
        return dict(
            north = self.north_,
            south = self.south_,
            west = self.west_,
            east = self.east_,
        )

    def latitudes(self):
        return [self.south_,self.north_]

    def longitudes(self):
        return [self.west_,self.east_]

    def __eq__(self,other):
        return self.west_ == other.west_ and self.north_ == other.north_ and self.east_ == other.east_ and self.south_ == other.south_

    def __str__(self):
        return ', '.join([ str(x) for x in self.coordinates_sn()])

    @classmethod
    def domains(self,application):
        if len(self.domains_) == 0:
            config = Configure(application)
            constants = config.file('constants.def','CONFIG','main')
            domains = ConfigFile(constants)
            for name,value in list(domains['domains'].items()):
                value = [ float(x) for x in value ]
                self.domains_[name] = Domain(*value)
        return self.domains_

def ValidateDomains(directive,keyword,values,*args):
    domains = Domain.domains(args[0])
    wrong = []
    for d in values:
        if not d in domains:
            wrong.append(d)
    if len(wrong) > 0:
        raise ValueError('The following domain(s) are unknown: %',', '.join(wrong))
    return values

def domainList(application):
    return list(Domain.domains(application).keys())
    

languageValidation.register('ValidateDomains',ValidateDomains)
