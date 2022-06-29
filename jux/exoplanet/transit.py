import numpy as np
import matplotlib.pyplot as plt

class TransitingExoplanet():
    """
    Class that accepts time, relative brightness and radius of the host star.
    """
    def __init__(self, time, fraw, radius_star):
        self.__time = np.array(time)
        self.__fraw = np.array(fraw)
        self.__radius_star = radius_star

        self.fcor = np.array([])
        self.__minimas = []
        self.radius = 0
        self.orbital_period = 0
        self.transit_duration = 0

    def correct_data(self, threshold_brightness):
        """
        Function correcting the raw relative brightness data.
        All values above threshold_brightness will be made equal to 1.
        """
        indices = np.where(abs(self.__fraw) > threshold_brightness)
        self.fcor = self.__fraw.copy()
        self.fcor[indices] = 1
        self.__find_minimas()
        self.__calc_radius()
        self.__calc_orbital_period()
        self.__calc_orbital_period()
        self.__calc_transit_duration()
    
    def __find_minimas(self):
        for i in range(1, len(self.fcor)-1):
            if (self.fcor[i-1]>self.fcor[i]) and (self.fcor[i]<self.fcor[i+1]):
                self.__minimas.append(i)

    def __calc_radius(self):
        depths = np.array([1-self.fcor[i] for i in self.__minimas])
        depth = np.average(depths)
        self.radius = self.__radius_star * np.sqrt(depth)

    def __calc_orbital_period(self):
        transit_days = []
        for i in range(1, len(self.__minimas)):
            transit_days.append(self.__time[self.__minimas[i]] - self.__time[self.__minimas[i-1]])
        transit_days = np.array(transit_days)
        self.orbital_period = np.average(transit_days)

    def __calc_transit_duration(self):
        __starting = []
        __ending = []
        __duration = []
        for i in range(1, len(self.fcor)):
            if (self.fcor[i]<1) and (self.fcor[i-1]==1):
                __starting.append(i-1)
            elif (self.fcor[i]==1) and (self.fcor[i-1]<1):
                __ending.append(i)
        for i in range(len(__starting)):
            __duration.append(self.__time[__ending[i]] - self.__time[__starting[i]])
        self.transit_duration = np.average(np.array(__duration))

    def plot_raw_data(self):
        """
        Plotting the raw relative brightness of the star.
        """
        plt.figure(figsize=(30, 10))
        plt.plot(self.__time, self.__fraw)
        plt.title('Exoplanet\'s parent star raw brightness')
        plt.xlabel('Time (in days)')
        plt.ylabel('Relative brightness')
        plt.grid()
        plt.show()

    def plot_corrected_data(self):
        """
        Plotting the corrected relative brightness of the star.
        """
        plt.figure(figsize=(30, 10))
        plt.plot(self.__time, self.fcor)
        plt.title('Exoplanet\'s parent star corrected brightness')
        plt.xlabel('Time (in days)')
        plt.ylabel('Relative brightness')
        plt.grid()
        plt.show()