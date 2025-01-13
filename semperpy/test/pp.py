from semperpy.gmao.gmao_config import GMAOConfig
from semperpy.fields.netcdf.file import File

config = GMAOConfig(verbose=10)
r = File('verif.nc',config)
fs = r.all_fields()
for f in fs:
    print(f.metadata())
