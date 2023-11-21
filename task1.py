from tqdm import tqdm
import time
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
    #load some files
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
    print(click_position)
    restored = np.copy(wavsignal)
    for i in tqdm(click_position, desc="Applying Median Filter"):
        start = max(i - window_length // 2, 0)
        end = min(i + window_length // 2 + 1, len(wavsignal))
        restored[i] = find_median(wavsignal[start:end])
    plt.figure(2) 
    plt.plot(restored)
    plt.show()
    print("Done!")
wavfile.write('output.wav', sample_rate1, restored)
#compute MSE
def mse(a, b):
    result = np.mean((a - b) ** 2)
    return result
sample_rate2, cleansignal = wav.read('realrealreal_clean.wav')
cleansignal = cleansignal / 32678
plt.figure(3)
plt.plot(cleansignal)
plt.show()
error = mse(cleansignal, restored)
error = f"{error:.10f}"
print(error)