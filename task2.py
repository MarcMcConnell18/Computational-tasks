from tqdm import tqdm
import time
import sounddevice as sd
from scipy.interpolate import CubicSpline
from scipy.io import wavfile
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import numpy as np


def find_median(numbers):
    numbers.sort()
    n = len(numbers)
    middle = n // 2
    return numbers[middle]


window_length = 9
if window_length % 2 == 0:
    print("Please input an odd number for window length!")
else:
    # load some files
    sample_rate1, wavsignal = wav.read('degraded.wav')
    wavsignal = wavsignal / 32678
    plt.figure(1)
    plt.plot(wavsignal)
    plt.show()
    position = np.loadtxt('click_position.csv', delimiter=',')
    position = position - 1
    position = position.astype(np.int32)
    np.save('position.npy', position)
    click_position = np.load('position.npy')
    restored = np.copy(wavsignal)
    # apply cubic spline and calculate execution time
    start_time = time.time()
    non_noise_index = [i for i in range(
        len(restored)) if i not in click_position]
    cs = CubicSpline(non_noise_index, restored[non_noise_index])
    restored[click_position] = cs(click_position)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"The execution time is {elapsed_time}s")
    sd.play(wavsignal, sample_rate1)
    sd.wait()
    sd.play(restored, sample_rate1)
    sd.wait
    plt.figure(2)
    plt.plot(restored)
    plt.show()

# compute MSE


def mse(a, b):
    result = np.mean((a - b) ** 2)
    return result


sample_rate2, cleansignal = wav.read('realrealreal_clean.wav')
cleansignal = cleansignal / 32678
error = mse(cleansignal, restored)
error = f"{error:.10f}"
print("The MSE is:", error)
