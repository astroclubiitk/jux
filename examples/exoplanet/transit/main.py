import pandas as pd
from jux.exoplanet import TransitingExoplanet

R = 7e8

df = pd.read_csv('transit_data.csv')
time = df[df.columns[0]]
fraw = df[df.columns[1]]

exoplanet = TransitingExoplanet(time, fraw, R)
exoplanet.plot_raw_data()

exoplanet.correct_data(threshold_brightness=0.998)
exoplanet.plot_corrected_data()

print("Radius of the planet is {} km".format(int(exoplanet.radius / 1000)))
print("The planet orbits around it's host star every {} Earth days".format(round(exoplanet.orbital_period, 2)))
print("The transit duration of the exoplanet is {} hours".format(round(exoplanet.transit_duration, 2)))