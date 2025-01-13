from netCDF4 import Dataset

f = Dataset('http://goldsmr3.sci.gsfc.nasa.gov:80/dods/MAI3CPASM')
t = f.variables['t']
print(t.missing_value)
print(t[:][0,0,:,:])
