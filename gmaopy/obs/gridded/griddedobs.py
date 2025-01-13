import _gridded_obs as gridded

class GriddedObs(object):

    def __init__(self,lonstep,latstep,west=-180,north=90.0,east=180.0,south=-90.0):
        if (east - west) % lonstep != 0:
            raise ValueError('The longitude step (%f) should be a multiple of the longitude span (%f)' % (lonstep,east - west))
        if (north - south) % latstep != 0:
            raise ValueError('The latitude step (%f) should be a multiple of the latitude span (%f)' % (latstep,north - south))
        self.lonstep_ = lonstep
        self.latstep_ = latstep
        if east > 180:
            east -= 180
            west -= 180
        self.west_ = west
        self.north_ = north
        self.east_ = east
        self.south_ = south

    def __call__(self,lats,lons,values):
        lats = self.checkContiguous(lats)
        lons = self.checkContiguous(lons)
        values = self.checkContiguous(values)
        latfilter = np.logical_and(lats >= self.south_,lats <= self.north_)
        lonfilter = np.logical_and(lons >= self.west_,lons < self.east_)
        filter = np.logical_and(latfilter,lonfilter)
        lats = lats[filter]
        lons = lons[filter]
        values = values[filter]

    def checkContiguous(self,a):
        if not a.flags.contiguous:
            a = numpy.ascontiguousarray(a)
        return a
