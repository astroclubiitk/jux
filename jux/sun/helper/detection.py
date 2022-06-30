import numpy as np
import matplotlib.pyplot as plt

from .params import THRESHOLD_SLOPE, MIN_COUNT_RATE_DIFF, MIN_TIME_DIFF

class DetectFlares():
    """
    Class that accepts preprocessed time and count rate as arguments.
    Finds out the data regarding the identified flares' start, peak and end times in the dataset.

    Implements Multi-Stage peak detection algorithm to detect the solar flares.
    """
    def __init__(self, time, rate):
        self.time, self.rate = time, rate
        self.s1, self.p1 = self.__calc_extremas()
        self.s2, self.p2 = self.__pair_extremas()
        self.s3, self.p3 = self.__slope_thresholding()
        self.s4, self.p4 = self.__filter_close()
        self.s5, self.p5 = self.__height_thresholding()
        self.e1 = self.__detect_ends()

    def __calc_extremas(self):
        s = []
        p = []
        if (self.rate[0]<=self.rate[1]):
            s.append(0)
        for i in range(1, len(self.time)-1):
            if (self.rate[i-1]<self.rate[i]) and (self.rate[i]>self.rate[i+1]):
                p.append(i)
            elif (self.rate[i-1]>self.rate[i]) and (self.rate[i]<self.rate[i+1]):
                s.append(i)
        if (self.rate[-2]>=self.rate[-1]):
            s.append(len(self.rate)-1)
        return s, p
    
    def __pair_extremas(self):
        s = []
        p = []
        for i in range(len(self.p1)):
            for j in range(len(self.s1)-1):
                if (self.time[self.s1[j+1]] > self.time[self.p1[i]]):
                    s.append(self.s1[j])
                    p.append(self.p1[i])
                    break
        return s, p

    def __slope_thresholding(self):
        s = []
        p = []
        for _s, _p in zip(self.s2, self.p2):
            slope = (self.rate[_p]-self.rate[_s]) / (self.time[_p]-self.time[_s])
            if (slope > THRESHOLD_SLOPE):
                s.append(_s)
                p.append(_p)
        return s, p

    def __filter_close(self):
        s = []
        p = []
        i = 0
        while (i < len(self.p3)):
            j = i+1
            while (j < len(self.p3)):
                if (self.rate[self.p3[j]]-self.rate[self.p3[i]] > MIN_COUNT_RATE_DIFF) or (self.time[self.p3[j]]-self.time[self.p3[i]] > MIN_TIME_DIFF):
                    break
                j += 1
            s.append(self.s3[i])
            p.append(self.p3[j-1])
            i = j
        return s, p

    def __height_thresholding(self):
        s = []
        p = []
        heights = np.array([(self.rate[self.p4[i]]-self.rate[self.s4[i]]) for i in range(len(self.p4))])
        avg_height = np.average(heights)
        for i in range(len(heights)):
            if (heights[i] > avg_height):
                s.append(self.s4[i])
                p.append(self.p4[i])
        return s, p

    def __detect_ends(self):
        e = []
        for i in range(len(self.p5)):
            for j in range(self.p5[i], len(self.rate)):
                if (i == len(self.p5)-1):
                    if (self.time[self.s1[-1]] < self.time[self.p5[i]]):
                        e.append(len(self.rate)-1)
                        break
                    elif (j == len(self.rate)-1):
                        e.append(len(self.rate)-1)
                if (self.rate[j] < (self.rate[self.p5[i]]+self.rate[self.s5[i]])/2):
                    e.append(j)
                    break
                if (i+1 < len(self.s5)):
                    if (self.time[j] > self.time[self.s5[i+1]]):
                        e.append(j-1)
                        break
        return e

    def plot(self):
        plt.figure(figsize=(30, 10))
        plt.title('Solar Activity')
        plt.plot(self.time, self.rate)
        plt.plot([self.time[i] for i in self.s5], [self.rate[i] for i in self.s5], 'x')
        plt.plot([self.time[i] for i in self.p5], [self.rate[i] for i in self.p5], 'o')
        plt.plot([self.time[i] for i in self.e1], [self.rate[i] for i in self.e1], 'x')
        plt.xlabel('Time (in s)')
        plt.ylabel('Count Rate')
        plt.grid()
        plt.show()