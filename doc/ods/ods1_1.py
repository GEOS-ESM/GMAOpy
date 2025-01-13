from gmaopy.ods.ods import ODS

reader = ODS('e561_tst_02.diag_conv.20110201_00z.ods')
filter = reader.compile('(kt == 4) & (kx == 289)', used_observations = False)
print(filter.shape)

# extract and filters from the file
obs = reader.read('obs',filter)
print(obs.shape,obs.mean())

# extract and filters from the file
filter = reader.compile('(kt == 4) & (kx == 289) & (qcexcl == 1)', used_observations = False)
obs = reader.read('obs',filter)
print(obs.shape,obs.mean())
