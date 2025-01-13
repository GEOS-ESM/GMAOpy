from semperpy.gmao.gmao_config import GMAOConfig
from semperpy.fields.netcdf.file import File

config = GMAOConfig(ignore_missing=True,verbose=11)
#r = File('http://opendap.nccs.nasa.gov:9090/dods/GEOS-5/fp/0.5_deg/fcast/inst3d_met_p/inst3d_met_p.20101009_00z',config)
#r = File('http://goldsmr3.sci.gsfc.nasa.gov:80/dods/MAI3CPASM',config)
r = File('/Users/claudegibert/Desktop/GMAOPortal/das/Y2010/M07/D09/d520_fp.inst3d_met_p.20100709_0000z.hdf',config)
a,f = r.slice(
    dict(
        parameter = 'h',
        level = 500,
        lat = [-90,90],
        lon = [0,360],
    )
)
b,g = r.slice(
    dict(
        parameter = 'h',
        level = 500,
        lat = [-90,90],
        lon = [0,360],
    )
)
print(a[0][:20])
print(b[0][:20])
