# import numpy and pyplot modules

import numpy as np

import matplotlib.pyplot as plot

# Create sine wave1

time = np.arange(0, 100, 0.1)

sinewave1 = np.sin(time)

# Create sine wave2 as replica of sine wave1

time1 = np.arange(0, 100, 0.1)

sinewave2 = np.sin(time1)

# Plot the sine waves - subplot 1

plot.title('Two sine waves with coherence as 1')

plot.subplot(211)

plot.grid(True, which='both')

plot.xlabel('time')

plot.ylabel('amplitude')

plot.plot(time, sinewave1, time1, sinewave2)

# Plot the coherence - subplot 2

plot.subplot(212)

coh, f = plot.cohere(sinewave1, sinewave2, 256, 1. / .01)

print("Coherence between two signals:")

print(coh)

print("Frequncies of the coherence vector:")

print(f)

plot.ylabel('coherence')

plot.show()

# ////////////////////////////////////////////////////////////////////////////////////////////////////////

# import numpy and pyplot

import numpy as np

import matplotlib.pyplot as plot

# Get x values of the sine wave one

time = np.arange(0, 100, 0.1);

# Create sine wave one

sinewave1 = np.sin(time)

# Get x values of the sine wave two

time1 = np.arange(0, 100, 0.1);

# Create sine wave two

sinewave2 = np.sin(time1) + np.random.randn(len(time1))  # add white noise to the signal

# Plot the sine waves

plot.subplot(211)

plot.xlabel("Time")

plot.ylabel("Amplitude")

plot.plot(time, sinewave1, time1, sinewave2)

plot.subplot(212)

coh, f = plot.cohere(sinewave1, sinewave2, 256, 1. / .01)

print("Coherence between the sine wave one and sine wave two:")

print(coh)

print("Frequency vector:")

print(f)

plot.xlabel('Frequency')

plot.ylabel('Coherence')

plot.show()
