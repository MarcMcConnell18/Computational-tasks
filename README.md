# Two methods to restore the degraded audio

## High-level Description of the project
This assignment builds on Assignment I. We assume that we have successfully detected the clicks and we are applying different interpolation methods to restore the audio, such as
- median filtering
- cubic splines
---
## Requirements
- Python 3.11.5
- Libraries: 'numpy','scipy','matplotlib','sounddevice','tqdm'
---

## Installation and Execution

Ensure Python 3.11.5 is installed on your system. Then install the required libraries using pip:
```sh                                 
pip install numpy
pip install scipy
pip install matplotlib
pip install sounddevice
pip install tqdm
```
For more details check [here](https://pypi.org/project/numpy/) for installing numpy
For more details check [here](https://pypi.org/project/scipy/) for installing scipy
For more details check [here](https://pypi.org/project/matplotlib/) for installing matplotlib
For more details check [here](https://pypi.org/project/sounddevice/) for installing sounddevice
For more details check [here](https://pypi.org/project/tqdm/) for installing tqdm

## Usage
1. Place the degraded audio file('degraded.wav') and the clean audio file(realrealreal_clean.wav) in the same directory as the script.
2. The script expects a CSV file ('click_position.csv') containing the positions of clicks in the audio file.
3. Run the script using Python:
```sh
python demo_audio_restoration.py
```
## Features
- Median Filtering: Removes clicks by applyng a median filter to the identified click positions in the audio sigal.
- Cubic Spline Interpolation: Restores the audio signal at the click positions using cubic spline interpolation.
- Performance Metrics: Calculates the Mean Squared Error (MSE) between the restored and original clean audio signals.
- Visualization: Plots the degraded signal and the restored signals using both methods for comparison.
- Unit Testing: Includes a unit test for the median number finding function.

## Configuration
- The window length for both median filtering and cubic spline can be adjusted in the script. Actually I made a test to window length, and turned out to be 3 is the best, which has the least MSE.
- Make sure the sample rate of the 'degraded.wav' and 'realrealreal_clean.wav' file are matched.
---

## Methodology and Results

**Methodology**
1. Data loading and preparation
- I load the audio file('degraded.wav' and 'realrealreal_clean.wav') and normalize its signal
- I also load CSV file ('click_position.csv') which containing the positions of the clicks in the audio signal
- The positions are adjusted by minus 1 and saved as a NumPy file, which is reload for further processing
2. Utility functions
Here I create 2 functions for using.
- 'fing_median': This function calculates the median of a given list of numbers, which is a crucial part of the median filtering process.
- 'mse': This function calculates the Mean Squared Error between two signals, used later to evaluate the restoration's accuracy.
3. Restoration
- Median Filter: I iterate through each position of the click and apply the median filter. This is done by taking a small window around each click, finding the median of the values in this window, and replacing the click value with this median. Also, I use a progress bar from 'tqdm' to visually indicate the process.
- Cubic Spline Interpolation: For each click position, a small window of values around the click is taken, and a cubic spline is fitted to these values. First I give x vector which is the sequence order of the data I need to process. Then I give y vector which are the value contain a click. The cubic spline is then used to estimate a smoother value at the click position. At last, I replace the click value by the estimated value.
4. Performance evaluation
The Mean Squared Error (MSE) between the restored signal and clean audio signal is calculated for both restoration methods. This offers a quantitative measure of how well each method performed.
5. Unit test
There is a unit test class 'TestMedianFunctions' which currently contains a single test case for the 'find_median' function. This is to test whether the function is correct or not.

**Results**

1. Find the best window length 
For the median filter, different lengths were explored to test the effectiveness of the restoration. In particular, from 3 to 35, every odd number was tested and 3 was observed to deliver the lowest MSE, which is 0.0041697141. 
For the cubic spline filter, I use the same numbers to test the MSE. 3 also is the best, the lowest MSE is 0.0034245923. 
The comparison of two methods is as shown in the figure below.

![mse_compare](https://i.imgur.com/ZsGPxHd.png)

2. Using the median filter and cubic spline filter
The result of two filters is shown below. We can clear see that all the clicks are removed and the restored audio signals are look same as the clean audio signal.
![results_signal](https://i.imgur.com/IYQprhE.png)

3. MSE and runtime
The MSE for median filter is 0.0041697141 and the MSE for cubic spline is 0.0034245923.
Comparing the two different interpolation methods, we notice that method cubic spline achieves a lower MSE.
The runtime of median filter method is 0.004983425140380859s, the runtime of cubic spline method is 0.014949560165405273s.

4. Listen
After listening to the two restored files, we notice that all the clicks has been removed and the results of two filters sounds like no difference.

---
## Credits

This code was developed for purely academic purposes by MarcMcConnell118 (Yujie Jia) as part of the module COMPUTATIONAL METHODS.

Resources:
- Brownrigg, David RK. "The weighted median filter." Communications of the ACM 27.8 (1984): 807-818.
- McKinley, Sky, and Megan Levine. "Cubic spline interpolation." College of the Redwoods 45.1 (1998): 1049-1060.




