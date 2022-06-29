import numpy as np
import matplotlib.pyplot as plt
from .helper import get_slope
from .params import MIN_MULTIPLIER, THRESHOLD_Y_NOISE_LVL5, THRESHOLD_X_NOISE_LVL5

"""Getting extremas functions"""

class MinMax():
    """
    Class that implements MultiStage peak detection algorithm to identify the peaks, start times
    and the end times of the solar flares present in the preprocessed lightcurve file.
    """

    def __init__(self,time, rate):
        self.l0_min, self.l0_max = self.level0_detect(np.array(time), np.array(rate))
        self.l1_min, self.l1_max = self.level1_detect(np.array(time), np.array(rate))
        self.l2_min, self.l2_max = self.level2_detect(np.array(time), np.array(rate))
        self.l3_min, self.l3_max = self.level3_detect(np.array(time), np.array(rate))
        self.l4_min, self.l4_max = self.level4_detect(np.array(time), np.array(rate))
        self.l5_min, self.l5_max = self.level5_detect(np.array(time), np.array(rate))
        self.l0_endt = self.level0end(np.array(time), np.array(rate))
        self.l1_endt = self.level1_end(np.array(time), np.array(rate))

    def level0_detect(self, xnew, ynew, should_plot=False):
        """
        Detection of all Minimas and Maximas
        """

        _s0 = []
        _p0 = []
        if ynew[0] <= ynew[1]:
            _s0.append(0)
        for i in range(1, len(ynew) - 1):
            if (ynew[i] > ynew[i - 1]) and (ynew[i] > ynew[i + 1]):
                _p0.append(i)
            elif (ynew[i] < ynew[i - 1]) and (ynew[i] < ynew[i + 1]):
                _s0.append(i)
        if ynew[-2] >= ynew[-1]:
            _s0.append(len(xnew) - 1)
        if should_plot:
            plt.figure(figsize=(30, 10))
            plt.title("Level 0 Maximas")
            plt.plot([xnew[i] for i in _p0], [ynew[i] for i in _p0], "o", xnew, ynew)
            plt.show()
            plt.figure(figsize=(30, 10))
            plt.title("Level 0 Minimas")
            plt.plot([xnew[i] for i in _s0], [ynew[i] for i in _s0], "o", xnew, ynew)
            plt.show()
        return _s0, _p0


    def level1_detect(self, xnew, ynew, should_plot=False):
        _s1 = []
        _p1 = []
        for i in range(len(self.l0_max)):
            for j in range(len(self.l0_min) - 1):
                # pairing of minimas and maximas as starts and peaks
                if xnew[self.l0_min[j + 1]] > xnew[self.l0_max[i]]:
                    _s1.append(self.l0_min[j])
                    _p1.append(self.l0_max[i])
                    break
        if should_plot:
            plt.figure(figsize=(30, 10))
            plt.title("Level 1 Maximas")
            plt.plot([xnew[i] for i in _p1], [ynew[i] for i in _p1], "o", xnew, ynew)
            plt.show()
            plt.figure(figsize=(30, 10))
            plt.title("Level 1 Minimas")
            plt.plot([xnew[i] for i in _s1], [ynew[i] for i in _s1], "o", xnew, ynew)
            plt.show()
            print(len(_s1))
        return _s1, _p1


    def level2_detect(self, xnew, ynew, should_plot=False):
        _s2 = []
        _p2 = []
        _slopes = np.array(
            [
                get_slope(xnew[self.l1_min[i]], xnew[self.l1_max[i]], ynew[self.l1_min[i]], ynew[self.l1_max[i]])
                for i in range(len(self.l1_min))
            ]
        )
        mean_sl = np.mean(_slopes)
        for i in range(len(self.l1_min)):
            # slope thresholding, the "significant" flares rise slopes are larger than mean rise
            if _slopes[i] > mean_sl:
                _s2.append(self.l1_min[i])
                _p2.append(self.l1_max[i])
        if should_plot:
            plt.figure(figsize=(30, 10))
            plt.title("Level 2 Maximas")
            plt.plot([xnew[i] for i in _p2], [ynew[i] for i in _p2], "o", xnew, ynew)
            plt.show()
            plt.figure(figsize=(30, 10))
            plt.title("Level 2 Minimas")
            plt.plot([xnew[i] for i in _s2], [ynew[i] for i in _s2], "o", xnew, ynew)
            plt.show()
            print(len(_s2))
        return _s2, _p2


    def level3_detect(self, xnew, ynew, f, should_plot=False):
        _s3 = []
        _p3 = []
        # setting a height threshold
        _std = np.std(np.array([ynew[self.l2_max[i]] - ynew[self.l2_min[i]] for i in range(len(self.l2_min))]))
        for i in range(len(self.l2_min)):
            if ynew[self.l2_max[i]] - ynew[self.l2_min[i]] > _std * f:  #! Hyperparameter
                _s3.append(self.l2_min[i])
                _p3.append(self.l2_max[i])
        if should_plot:
            plt.figure(figsize=(30, 10))
            plt.title("Level 3 Maximas")
            plt.plot([xnew[i] for i in _p3], [ynew[i] for i in _p3], "o", xnew, ynew)
            plt.show()
            plt.figure(figsize=(30, 10))
            plt.title("Level 3 Minimas")
            plt.plot([xnew[i] for i in _s3], [ynew[i] for i in _s3], "o", xnew, ynew)
            plt.show()
        return _s3, _p3


    def level4_detect(self, xnew, ynew, should_plot=False):
        _s4 = []
        _p4 = []
        s = set()
        for i in range(len(self.l3_min)):
            # appending and pairing unique starts and peaks
            if self.l3_min[i] in s:
                continue
            s.add(self.l3_min[i])
            _s4.append(self.l3_min[i])
            _p4.append(self.l3_max[i])
        if should_plot:
            plt.figure()
            plt.title("Final Start and Peak")
            plt.plot(
                [xnew[i] for i in _p4],
                [ynew[i] for i in _p4],
                "o",
                [xnew[i] for i in _s4],
                [ynew[i] for i in _s4],
                "x",
                xnew,
                ynew,
            )
            plt.show()
        return _s4, _p4


    def level5_detect(self, xnew, ynew, should_plot=False):
        # a filter for too close peaks
        li = []
        for i in range(len(self.l4_max) - 3):
            if (xnew[self.l4_max[i + 1]] - xnew[self.l4_max[i]] < THRESHOLD_X_NOISE_LVL5) and (
                np.abs(ynew[self.l4_max[i + 1]] - ynew[self.l4_max[i]]) < THRESHOLD_Y_NOISE_LVL5
            ):
                if ynew[self.l4_max[i + 1]] > ynew[self.l4_max[i]]:
                    li.append(i)
                elif ynew[self.l4_max[i + 1]] < ynew[self.l4_max[i]]:
                    li.append(i+1)
        for index in sorted(li, reverse=True):
            del self.l4_min[index]
            del self.l4_max[index]
        if should_plot:
            plt.figure(figsize=(30, 10))
            plt.title("Final Start and Peak")
            plt.plot(
                [xnew[i] for i in self.l4_max],
                [ynew[i] for i in self.l4_max],
                "o",
                [xnew[i] for i in self.l4_min],
                [ynew[i] for i in self.l4_min],
                "x",
                xnew,
                ynew,
            )
            plt.show()
        return self.l4_min, self.l4_max


    def level0_end(self, xnew, ynew, should_plot=False):
        _e0 = []
        for i in range(len(self.l4_max)):
            for j in range(self.l4_max[i], len(xnew)):
                # edge case for the last peak's end
                if i == len(self.l4_max) - 1:
                    if xnew[self.l0_min[-1]] < xnew[self.l4_max[i]]:
                        _e0.append(len(xnew) - 1)
                        break
                    elif j == len(xnew) - 1:
                        _e0.append(len(xnew) - 1)
                # usual ends with definition of being midway the intensity of peak and start
                if ynew[j] < (ynew[self.l4_max[i]] + ynew[self.l4_min[i]]) / 2:
                    _e0.append(j)
                    break
                if i + 1 < len(self.l4_min):
                    if xnew[j] > xnew[self.l4_min[i + 1]]:
                        _e0.append(j - 1)
                        break
        if should_plot:
            plt.figure()
            plt.title("Level 0 Ends")
            plt.plot(
                [xnew[i] for i in self.l4_max],
                [ynew[i] for i in self.l4_max],
                "o",
                [xnew[i] for i in _e0],
                [ynew[i] for i in _e0],
                "x",
                xnew,
                ynew,
            )
            plt.show()
        return _e0


    def level1_end(self, xnew, ynew,should_plot=False):
        _e1 = []
        for i in range(len(self.l0_endt)):
            # for each _e0
            if ynew[self.l0_endt[i]] < ynew[self.l4_max[i]]:
                _e1.append(self.l0_endt[i])
            else:
                # if intensity of end > its peak
                # find the next minima that has it's reverse true
                for j in range(len(self.l0_min)):
                    if xnew[self.l0_min[j]] > xnew[self.l4_max[i]]:
                        if ynew[self.l0_min[j + 1]] > ynew[self.l0_min[j]]:
                            _e1.append(self.l0_min[j])
                            break
        if should_plot:
            plt.figure()
            plt.title("Peaks and Ends")
            plt.plot(
                [xnew[i] for i in self.l4_max],
                [ynew[i] for i in self.l4_max],
                "o",
                [xnew[i] for i in _e1],
                [ynew[i] for i in _e1],
                "x",
                xnew,
                ynew,
            )
            plt.show()
        _e1 = np.array(_e1)
        return _e1