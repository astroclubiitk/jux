import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from .functions import linear_func, log_exp_func

class ModelFlares():
    """
    Class that accepts raw flare data and models into the Flare Profile.
    
    Also finds out the class of the flare.
    """
    def __init__(self, time, rate, start, peak, end):
        self.time = time
        self.rate = rate
        self.s = start
        self.p = peak
        self.e = end
        self.background = np.min(rate)
        self.s_calc = self.__calc_starts()
        self.e_calc = self.__calc_ends()
        self.classes = self.__classify()
        self.data = self.__generate_df()
    
    def __calc_starts(self):
        s_calc = []
        for i in range(len(self.s)):
            x_rise = self.time[self.s[i]:self.p[i]+1]
            y_rise = self.rate[self.s[i]:self.p[i]+1]
            popt, pcov = curve_fit(linear_func, x_rise, y_rise)
            m, c = popt
            s_calc.append(int((self.background - c) / m))
        return s_calc

    def __calc_ends(self):
        e_calc = []
        for i in range(len(self.p)):
            x_fall = self.time[self.p[i]:self.e[i]+1] - self.time[self.p[i]]
            y_fall = np.log(self.rate[self.p[i]:self.e[i]+1])
            popt, pcov = curve_fit(log_exp_func, x_fall, y_fall)
            ln_a, b = popt
            end_time = np.square((np.log(self.background) - ln_a) / (-1 * b)) + self.p[i]
            e_calc.append(int(end_time))
        return e_calc

    def __classify(self):
        classes = []
        for i in range(len(self.p)):
            peak_intensity = self.rate[self.p[i]]
            val = np.log10(peak_intensity / 25)
            _val = str(int(val*100) / 10)[-3:]
            c = ""
            if int(val) < 1:
                c = "A" + _val
            elif int(val) == 1:
                c = "B" + _val
            elif int(val) == 2:
                c = "C" + _val
            elif int(val) == 3:
                c = "M" + _val
            elif int(val) > 3:
                c = "X" + _val
            classes.append(c)
        return classes

    def __generate_df(self):
        start_intensities = [self.rate[i] for i in self.s]
        peak_intensities = [self.rate[i] for i in self.p]
        df = pd.DataFrame([self.s, self.p, self.e, self.s_calc, self.e_calc, start_intensities, peak_intensities, self.classes])
        df = df.T
        df.columns = ['Observed Start Time', 'Peak Time', 'Observed End Time', 'Calculated Start TIme', 'Calculated End Time', 'Pre-Flare Count Rate', 'Total Count Rate', 'Class']
        return df