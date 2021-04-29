import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft, fftfreq
from time import sleep

f = 10  # Frequency, in cycles per second, or Hertz
f_s = 1/115200 # Sampling rate, or number of measurements per second
num = 1000
t = np.linspace(0, 2, 2*100, endpoint = False)
print(len(t))
# t = np.arange(0,num)*f_s
y = np.sin(f * 2 * np.pi * t)

# Calculate the FFT
X = fft(y)
freqs = fftfreq(len(y), d = 1/100) # f_s could be 1/baudrate

 # print the positive frequency that has the most correlation
print(freqs[np.argmax(np.abs(X[0:int(len(X)/2)]))])
m = max(freqs)
l = len(freqs)
print(m)
print(l)
print(m/l)
print()

sleep(5)

while True:
    num += 1000
    t = np.arange(0,num)*f_s
    y = np.sin(f * 2 * np.pi * t)

    # Calculate the FFT
    X = fft(y)
    freqs = fftfreq(len(y), d = f_s) # f_s could be 1/baudrate

     # print the positive frequency that has the most correlation
    print(freqs[np.argmax(np.abs(X[0:int(len(X)/2)]))])
    m = max(freqs)
    l = len(freqs)
    print(m)
    print(l)
    print(m/l)
    print()

    # if m/l < 0.1:
    #     sleep(0.5)
###############
# Plot the data
###############
# fig, ax = plt.subplots()
# ax.plot(t, y)

fig2, ax2 = plt.subplots()

ax2.stem(freqs, np.abs(X))
ax2.set_xlabel('Frequency in Hertz [Hz]')
ax2.set_ylabel('Frequency Domain (Spectrum) Magnitude')
ax2.set_xlim(-f_s / 2, f_s / 2)
ax2.set_ylim(-5, 110)

plt.show()
