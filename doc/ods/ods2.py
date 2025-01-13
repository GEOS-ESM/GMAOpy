from gmaopy.ods.ods import ODS

reader = ODS('e561_tst_02.diag_conv.20110201_00z.ods')
filter = reader.compile('(kt == 4) & (kx == 289) & ((lat < -20) | (lat > 20))')
obs = reader.read('obs',filter)
print(obs.shape)
