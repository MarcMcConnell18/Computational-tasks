from tqdm import tqdm
import time
import unittest
import sounddevice as sd
from scipy.interpolate import CubicSpline
from scipy.io import wavfile
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import numpy as np

# load some files and set some parameters
sample_rate1, wavsignal = wav.read('degraded.wav')
wavsignal = wavsignal / 32678
position = np.loadtxt('click_position.csv', delimiter=',')
position = position - 1
position = position.astype(np.int32)
np.save('position.npy', position)
click_position = np.load('position.npy')
wavsignal1 = np.copy(wavsignal)
wavsignal2 = np.copy(wavsignal)
restored1 = np.copy(wavsignal)
restored2 = np.copy(wavsignal)
sample_rate2, cleansignal = wav.read('realrealreal_clean.wav')
cleansignal = cleansignal / 32678
cleansignal1 = np.copy(cleansignal)
cleansignal2 = np.copy(cleansignal)

# define some useful functions
# fine median number

def find_median(numbers):
    numbers.sort()
    n = len(numbers)
    middle = n // 2
    return numbers[middle]

# compute MSE


def mse(a, b):
    result = np.mean((a - b) ** 2)
    return result


###
# TASK 1 (use median filter)
window_length1 = 3
if window_length1 % 2 == 0:
    print("Please input an odd number for window length!")
else:
    start_time = time.time()
    for i in tqdm(click_position, desc="Applying Median Filter"):
        start1 = max(i - window_length1 // 2, 0)
        end1 = min(i + window_length1 // 2 + 1, len(wavsignal1))
        restored1[i] = find_median(wavsignal1[start1:end1])
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"The execution time is {elapsed_time}s")
    print("Done!")


# TASK 2 (use cubic splines)
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
        end = min(i + window_length2 // 2 + 1, len(wavsignal2))
        x = [k for k in range(1, window_length2+1)]
        x = np.array(x)
        y = wavsignal2[start:end]
        cs = CubicSpline(x, y)
        x_new = np.linspace(x.min(), x.max(), 1)
        y_new = cs(x_new)
        restored2[i] = y_new[0]
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"The execution time is {elapsed_time}s")
    plt.figure(2)
    plt.subplot(2, 3, 1)
    plt.xlabel('Spot number')
    plt.ylabel('Amplitude')
    plt.title('Degraded audio signal')
    plt.plot(wavsignal)
    plt.subplot(2, 3, 2)
    plt.xlabel('Spot number')
    plt.ylabel('Amplitude')
    plt.title('Restored audio by median filter')
    plt.plot(restored1)
    plt.subplot(2, 3, 3)
    plt.xlabel('Spot number')
    plt.ylabel('Amplitude')
    plt.title('Clean audio signal')
    plt.plot(cleansignal)
    plt.subplot(2, 3, 4)
    plt.xlabel('Spot number')
    plt.ylabel('Amplitude')
    plt.title('Degraded audio signal')
    plt.plot(wavsignal)
    plt.subplot(2, 3, 5)
    plt.xlabel('Spot number')
    plt.ylabel('Amplitude')
    plt.title('Restored audio by cubic spline')
    plt.plot(restored2)
    plt.subplot(2, 3, 6)
    plt.xlabel('Spot number')
    plt.ylabel('Amplitude')
    plt.title('Clean audio signal')
    plt.plot(cleansignal1)
    plt.show()

# compute MSE
error1 = mse(cleansignal1[click_position], restored1[click_position])
error1 = f"{error1:.10f}"
error2 = mse(cleansignal2[click_position], restored2[click_position])
error2 = f"{error2:.10f}"
print("The MSE for median filter is:", error1)
print("The MSE for cubic spline is:", error2)

# store the output audio
wavfile.write('output_medianfilter.wav', sample_rate1, restored1)
wavfile.write('output_cubicspline.wav', sample_rate1, restored2)

# play the audio
# sd.play(wavsignal, sample_rate1)
# sd.wait()
# sd.play(restored1, sample_rate1)
# sd.wait()
# sd.play(restored2, sample_rate1)
# sd.wait()


# unit test


class TestMedianFunctions(unittest.TestCase):
    def test_find_median_odd(self):
        self.assertEqual(find_median([3, 1, 2]), np.median([3, 1, 2]))


if __name__ == '__main__':
    unittest.main()
