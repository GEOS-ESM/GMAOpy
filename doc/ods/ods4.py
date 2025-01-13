from gmaopy.ods.ods import ODS

reader = ODS('e561_tst_02.diag_conv.20110201_00z.ods')
filter = reader.compile('(kx == 289) & (kt == 4) & ((obs-omf) < 0)')
o = reader.read('obs',filter)
print(o.shape)
filter = reader.compile('(kx == 289) & (kt == 4) & ((obs-omf) >= 0)')
o = reader.read('obs',filter)
print(o.shape)
filter = reader.compile('(kx == 289) & (kt == 4)')
o = reader.read('obs',filter)
print(o.shape)
