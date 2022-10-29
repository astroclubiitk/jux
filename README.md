# JUX

<img align="right" style="padding-left: 20px" width="190" height="auto" src="./assets/logo.jpg">

This project is concerned with processing and identification of features present in astronomical light data, often referred to as lightcurve data. It was created in response to 2 ocassions:
- ISRO Problem Statement: Inter-IIT Tech Meet 10.0
- XUVI: Summer Project, Astronomy Club IITK, 2022    

## How to install it?
```sh
pip install jux
```
Dependencies will build and you can proceed using it.

## What all can it process?
Currently, feature detection is supported for:
- Exoplanet detection
    - Transit Photometry
    - Astrometry
- Solar Flare detection

## How to use it?
Sample data can be downloaded <a href="https://github.com/astroclubiitk/jux/tree/main/examples" targer="_blank">here</a>.

### Exoplanet detection
1. Transit Photometry
```py
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
```

2. Astrometry
```py
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
```

### Solar Flare detection

```py
from jux.sun import Flares, read_lc_file

path_to_lc = 'ch2_xsm_20200928_v1_level2.lc'
time, rate = read_lc_file(path_to_lc)

flares = Flares(time, rate)
flares.identified.plot()
flares.print_details()
```