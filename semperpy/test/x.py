from semperpy.plot.matplotlib.layout import Layout
from gmaopy.ods.ods import ODS

reader = ODS('/Users/claudegibert/Desktop/obs/impact/Y2011/M03/D23/H00/e562p5_fp.imp3_txe_amsua_n19.obs.20110322_15z+20110324_00z-20110323_00z.ods')
filter = reader.compile('(kt == 40) & (kx == 319) & (lev == 5)')
omf = reader.extract('omf',filter)
xvec = reader.extract('xvec',filter)
print(omf.shape)
print(xvec.shape)
l = Layout([1,1],interactive=True)
subplot = l()
subplot.scatter(omf,xvec)
subplot.set_ylim(top=2e-4,bottom=-2e-4)
l.draw()
