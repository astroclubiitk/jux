from astropy.table import Table
from jux.sun.flares import Preprocessing

path_to_lc = 'ch2_xsm_20210909_v1_level2.lc'
table = Table.read(path_to_lc)

time = table['TIME']
rate = table['RATE']

data = Preprocessing(time, rate)
data.plot_interpolated_data()