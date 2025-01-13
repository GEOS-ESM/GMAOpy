from gmaopy.ods.ods import ODS

reader = ODS('e561_tst_02.diag_conv.20110201_00z.ods')
pressure = reader.compile('(kx == 181) & (kt == 33)')
europe = reader.compile('(lat > 35) & (lat < 75) & (lon > -12.5) & (lon < 42.5)')
namer = reader.compile('(lat > 20) & (lat < 60) & (lon > -140) & (lon < -60)')

# Station pressure in Europe (a)
obs = reader.read('obs',europe & pressure)
print(obs.shape)

# Station pressure in North America (b)
obs = reader.read('obs',namer & pressure)
print(obs.shape)

# Station pressure in North America or Europe (c)
obs = reader.read('obs',(europe | namer) & pressure)
print(obs.shape)

# Station pressure global (d)
obs = reader.read('obs',pressure)
print(obs.shape)

# Station pressure global except Europe (e)
obs = reader.read('obs',pressure & ~europe)
print(obs.shape)
