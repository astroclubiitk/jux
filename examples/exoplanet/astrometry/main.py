import pandas as pd
from jux.exoplanet import Star

M = 1e30

df = pd.read_csv('astrometry_data.csv')
time = df[df.columns[0]]
vel = df[df.columns[1]]

star = Star(time, vel, M)
star.plot_raw_fourier_transform()

star.correct_fourier_transform(threshold_power=50)
star.plot_individual_planet_influence()

for i in range(len(star.planets)):
    star.print_planet_details(i)
    print("")