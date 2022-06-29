import numpy as np
import matplotlib.pyplot as plt

from .params import *

class Star():
    """
    Class that accepts time, radial velocity and mass of the star as inputs.
    Calculates the details of the various exoplanets detected.
    """
    def __init__(self, time, raw_vel, mass):
        self.__time = np.array(time)
        self.__raw_vel = raw_vel
        self.__M = mass

        self.__raw_fourier_power, self.__fourier_freq = self.__calc_fourier_transform()
        self.__corrected_fourier_power = []
        self.__corrected_vel = []
        self.__planets_influence = []
        self.planets = []

    def __calc_fourier_transform(self):
        __power = np.fft.rfft(self.__raw_vel)
        __freq = np.fft.rfftfreq(len(self.__raw_vel), (self.__time[1]-self.__time[0]))
        return __power, __freq

    def correct_fourier_transform(self, threshold_power):
        """
        Function to process fourier transform based on threshold_power
        """
        self.__corrected_fourier_power = self.__raw_fourier_power.copy()
        zeros = np.where(np.abs(self.__raw_fourier_power) < threshold_power)
        self.__corrected_fourier_power[zeros] = 0
        self.__corrected_fourier_power[0] = 0
        self.__corrected_vel = np.fft.irfft(self.__corrected_fourier_power)
        self.__calc_planets_influence()
        self.__calc_planet_data()

    def __calc_planets_influence(self):
        indices = np.where(np.abs(self.__corrected_fourier_power) > 0)
        for i in indices[0]:
            __indices = np.where(np.abs(self.__corrected_fourier_power) != np.abs(self.__corrected_fourier_power[i]))
            __power = self.__corrected_fourier_power.copy()
            __power[__indices] = 0
            __inverse = np.fft.irfft(__power)
            self.__planets_influence.append(__inverse)

    def __calc_planet_data(self):
        for i in self.__planets_influence:
            v = i.max()
            __indices = []
            for j in range(1, len(i)-1):
                if (i[j-1]<i[j]) and (i[j]>i[j+1]):
                    __indices.append(j)
                if (len(__indices) == 2):
                    break
            t = self.__time[__indices[1]] - self.__time[__indices[0]]
            omega = 2 * np.pi / t
            R = v / omega
            x = np.cbrt((G * self.__M) / (v * v * R))
            r = (x+1) * R
            m = self.__M / (x+1)
            planet_data = {
                'radius_revolution': r+R,
                'mass': m,
                'omega_revolution': omega,
                'time_revolution': t
            }
            self.planets.append(planet_data)

    def print_planet_details(self, n):
        """
        Prints details of the n-th planet.
        """
        if (n>len(self.planets)) or (n<0):
            print("Exoplanet not found! Enter a number between 1 and {}".format(len(self.planets)+1))
            return
        print("Details of Exoplanet #{}:".format(n+1))
        print("    Mass of the Exoplanet     = {} Earth masses".format(round(self.planets[n]["mass"]/ME, 2)))
        print("    Radius of Revolution      = {} AU".format(round(self.planets[n]["radius_revolution"]/AU, 2)))
        print("    Time Period of Revolution = {} Earth years".format(round(self.planets[n]["time_revolution"]/(SPD*365), 2)))

    def plot_raw_vel(self):
        """
        Plotting raw velocity of the observed star.
        """
        plt.figure(figsize=(30, 10))
        plt.scatter(self.__time, self.__raw_vel, s=0.3)
        plt.xlabel('Time (in $s$)')
        plt.ylabel('Radial velocity (in $m/s$)')
        plt.title('Raw stellar velocity')
        plt.grid()
        plt.show()

    def plot_raw_fourier_transform(self):
        """
        Plotting fourier transform of the raw velocity.
        """
        plt.figure(figsize=(30, 10))
        plt.scatter(self.__fourier_freq, np.abs(self.__raw_fourier_power), s=0.3)
        plt.title('Fourier transform of raw stellar radial velocity')
        plt.title('Frequency (in $s^{-1}$)')
        plt.ylabel('Power')
        plt.grid()
        plt.show()

    def plot_corrected_fourier_transform(self):
        """
        Plotting the corrected fourier transform, after `correct_fourier_transform`.
        """
        plt.figure(figsize=(30, 10))
        plt.scatter(self.__fourier_freq, np.abs(self.__corrected_fourier_power), s=0.3)
        plt.title('Processed fourier transform of raw stellar radial velocity')
        plt.title('Frequency (in $s^{-1}$)')
        plt.ylabel('Power')
        plt.grid()
        plt.show()

    def plot_corrected_velocity(self):
        """
        Plotting the real inverse fourier transform of corrected fourier transform.
        """
        plt.figure(figsize=(30, 10))
        plt.plot(self.__time, self.__corrected_vel)
        plt.xlabel('Time (in $s$)')
        plt.ylabel('Radial velocity (in $m/s$)')
        plt.title('Corrected stellar velocity')
        plt.grid()
        plt.show()

    def plot_individual_planet_influence(self):
        """
        Plotting contribution of each planet towards the observed radial stellar velocity.
        """
        plt.figure(figsize=(30, 10))
        for __vel in self.__planets_influence:
            plt.plot(self.__time, __vel)
        plt.title('Planetary influence on stellar velocity')
        plt.xlabel('Time (in $s$)')
        plt.ylabel('Radial velocity (in $m/s$)')
        plt.grid()
        plt.show()