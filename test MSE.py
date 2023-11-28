from tqdm import tqdm
import time
from scipy.io import wavfile
from scipy.interpolate import CubicSpline
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import numpy as np
def find_median(numbers):
    numbers.sort()
    n = len(numbers)
    middle = n // 2
    return numbers[middle]

def mse(a, b):
    result = np.mean((a - b) ** 2)
    return result

sample_rate1, wavsignal = wav.read('degraded.wav')
wavsignal = wavsignal / 32678 
plt.figure(1)
plt.plot(wavsignal)     
plt.show()
sample_rate2, cleansignal = wav.read('realrealreal_clean.wav')
cleansignal = cleansignal / 32678
position = np.loadtxt('click_position.csv', delimiter=',')
position = position - 1
position = position.astype(np.int32)
np.save('position.npy', position)
click_position = np.load('position.npy')
restored1 = np.copy(wavsignal)
restored2 = np.copy(wavsignal)
window_length1= [3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35]
window_length2 = [3,5,7,9,11,13,15,17,19,21,23,25,27,29,31]
error1 = np.empty(len(window_length1))
error2 = np.empty(len(window_length2))
for j in range(len(window_length1)):
    if window_length1[j] % 2 == 0:
        print("Please input an odd number for window length!")
    else:
        for i in (click_position):
            start1 = max(i - window_length1[j] // 2, 0)
            end1 = min(i + window_length1[j] // 2 + 1, len(wavsignal))
            restored1[i] = find_median(wavsignal[start1:end1])
        #compute MSE
        error1[j] = mse(cleansignal[click_position], restored1[click_position])
for j in range(len(window_length2)):
    if window_length2[j] % 2 == 0:
        print("Please input an odd number for window length!")
    else:
        for i in (click_position):
            start2 = max(i - window_length2[j] // 2, 0)
            end2 = min(i + window_length2[j] // 2 + 1, len(wavsignal))
            x = [k for k in range(1, window_length2[j]+1)]
            x = np.array(x)
            y = wavsignal[start2:end2]
            cs = CubicSpline(x, y)
            x_new = np.linspace(x.min(), x.max(), 1)
            y_new = cs(x_new)
            restored2[i] = y_new
        error2[j] = mse(cleansignal[click_position], restored2[click_position])
plt.figure(2)
plt.subplot(2,1,1)
plt.plot(window_length1, error1, color='r', marker='*', linestyle='--', markersize=8,alpha=0.5, linewidth=3)
# plt.xticks(window_length1)
plt.xlabel(u'window length')
# plt.yticks(error1)
plt.ylabel(u'MSE')
plt.title(u'Compare MSE for median filter')
plt.figure(2)
plt.subplot(2,1,2)
plt.plot(window_length2, error2, color='b', marker='d', linestyle='-', markersize=8, alpha=0.5, linewidth=3)
plt.xlabel(u'window length')
# plt.yticks(error1)
plt.ylabel(u'MSE')
plt.title(u'Compare MSE for cubic spline')
plt.show()