from tqdm import tqdm
import time
import sounddevice as sd
from scipy.interpolate import CubicSpline
from scipy.io import wavfile
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import numpy as np

### load some files and set some parameters
sample_rate1, wavsignal = wav.read('degraded.wav')
wavsignal = wavsignal / 32678
position = np.loadtxt('click_position.csv', delimiter=',')
position = position - 1
position = position.astype(np.int32)
np.save('position.npy', position)
click_position = np.load('position.npy')
restored1 = np.copy(wavsignal)
restored2 = np.copy(wavsignal)
###

### define some useful functions
### fine median number
def find_median(numbers):
    numbers.sort()
    n = len(numbers)
    middle = n // 2
    return numbers[middle]
###
### TASK 1 (use median filter)
window_length1 = 3
if window_length1 % 2 == 0:
    print("Please input an odd number for window length!")
else:
    start_time = time.time()
    for i in tqdm(click_position, desc="Applying Median Filter"):
        start1 = max(i - window_length1 // 2, 0)
        end1 = min(i + window_length1 // 2 + 1, len(wavsignal))
        restored1[i] = find_median(wavsignal[start1:end1])
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"The execution time is {elapsed_time}s")
    print("Done!")


### TASK 2 (use cubic splines)
window_length2 = 3
if window_length2 % 2 == 0:
    print("Please input an odd number for window length!")
else:
    start_time = time.time()
    # non_noise_index = [i for i in range(
    #     len(restored)) if i not in click_position]
    # cs = CubicSpline(non_noise_index, restored[non_noise_index])
    # restored[click_position] = cs(click_position)
    for i in tqdm(click_position, desc="Applying Cubic Spline"):
        start = max(i - window_length2 // 2, 0)
        end = min(i + window_length2 // 2 + 1, len(wavsignal))
        x = [k for k in range(1, window_length2+1)]
        x = np.array(x)
        y = wavsignal[start:end]
        cs = CubicSpline(x, y)
        x_new = np.linspace(x.min(), x.max(), 1)
        y_new = cs(x_new)
        restored2[i] = y_new
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"The execution time is {elapsed_time}s")
    # sd.play(wavsignal, sample_rate1)
    # sd.wait()
    # sd.play(restored, sample_rate1)
    # sd.wait
    # plt.figure(2)
    # plt.plot(restored)
    # plt.show()

# compute MSE


def mse(a, b):
    result = np.mean((a - b) ** 2)
    return result


sample_rate2, cleansignal = wav.read('realrealreal_clean.wav')
cleansignal = cleansignal / 32678
error = mse(cleansignal[click_position], restored[click_position])
error = f"{error:.10f}"
print("The MSE is:", error)
