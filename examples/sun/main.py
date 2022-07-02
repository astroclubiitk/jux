from jux.sun import Flares, read_lc_file

path_to_lc = 'ch2_xsm_20200928_v1_level2.lc'
time, rate = read_lc_file(path_to_lc)

flares = Flares(time, rate)
flares.identified.plot()
flares.print_details()