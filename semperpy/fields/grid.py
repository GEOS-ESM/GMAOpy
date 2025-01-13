
class Grid(object):

    def __init__(self,latitudes,longitudes):
        self.latitudes_ = latitudes
        self.longitudes_ = longitudes
        self.bottom_ = latitudes[0]
        self.left_ = longitudes[0]
        self.top_ = latitudes[-1]
        self.right_ = longitudes[-1]
        self.latdim_ = None
        self.londim_ = None
        self.weights_ = None
        self.shape = (len(latitudes), len(longitudes))

    def rectangle(self):
        return self.left_,self.bottom_,self.right_,self.top_

    def longitudes(self):
        return self.longitudes_

    def latitudes(self):
        return self.latitudes_

    def weights(self):
        if self.weights_ == None:
            to_radians = 3.14159 / 180.0
            self.weights_ = np.cos(np.array(self.latitudes_) * to_radians)
            self.weights_ = np.repeat(self.weights_,len(self.longitudes_))
            self.weights_ = self.weights_.reshape((len(self.latitudes_),len(self.longitudes_)))
        return self.weights_

    def extract_subdomain(self,domain,values,missing_value):
        # Works for regular grids only
        # values is assumed to be a 2 dimensional array lat,lon
        if self.latdim_ == None: 
            self.createDimensions()
        lats = self.latdim_(domain.latitudes())
        lons = self.londim_(domain.longitudes())
        # we need to manually create this as more than one slice can be returned
        # longitude (e.g. usually overlap at either 0 or -180).
        lengths = [] 
        combinations = self.preFlight([lats,lons],lengths,)
        x = 0
        y = 0
        for v in lengths:
            x = v[0]
            y += v[1]
        domain = ma.zeros((x,y),dtype=values.dtype)
        domain = ma.masked_values(domain,missing_value,copy=False,shrink=True)
        for pair in combinations:
            domain[pair[1]] = values[pair[0]]
        return domain

    def preFlight(self,slices,lengths,src=[],dst=[]):
        result = []
        if len(slices) == 0:
            lengths.append([dst[0].stop - dst[0].start,dst[1].stop - dst[1].start])
            result = [[src,dst]]
        else:
            value = slices[0]
            start = 0
            for v in value:
                vlen = v.stop-v.start
                dest = slice(start,start + vlen)
                result += self.preFlight(slices[1:],lengths,src + [v],dst + [dest])
                start += vlen
        return result

    def extract_grid(self,domain):
        if self.latdim_ == None: 
            self.createDimensions()
        lats = []
        slices = self.latdim_(domain.latitudes())
        for s in slices:
            lats += self.latdim_.slice(s)
        lons = []
        slices = self.londim_(domain.longitudes())
        for s in slices:
            lons += self.londim_.slice(s)
        if len(slices) > 1:
            # we went over the longitude overlap, we 'shift' the values
            for i in range(len(lons)):
                if lons[i] < 0:
                    lons[i] += 360
        return NGrid(lats,lons)

    def createDimensions(self):
        self.latdim_ = LatitudeIndex("lat",self.latitudes_,True,True)
        self.londim_ = LongitudeIndex("lon",self.longitudes_,True,True)

