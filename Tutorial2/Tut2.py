import numpy as np
import matplotlib.pylab as plt
from scipy import fftpack


frcy = 200
smpl_rate = 50
t = np.linspace(0,2,2*smpl_rate, endpoint=False)
x = np.sin(frcy*2*np.pi*t)
# fig, ax = plt.subplots()
# ax.plot(t,x)
# plt.show()

X= fftpack.fft(x)
freqs = fftpack.fftfreq(len(x)) * smpl_rate

fig, ax = plt.subplots()

ax.plot(freqs, np.abs(X))
ax.set_xlabel('Frequency in Hertz [Hz]')
ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
ax.set_xlim(-300, 300)
ax.set_ylim(-5, 110)
plt.show()


# x = np.linspace(-np.pi, np.pi, 201)
# plt.plot(x, np.sin(x))
# plt.show()
#
# def plotSpectrum(y, sampleRate):
#     length = len(y)
#     num_range = arange(length)
#     T = length/sampleRate
#     frequency = num_range/T #2 sides
#     frequency = frequency[range(length/2)] # one side
#
#     Y = fft(y)/length
#     Y = Y[range(length/2)]
#
#
#     plt.plot(frequency, abs(Y), 'r')
#
# sampleRate = 200.0
# interval = 1.0/sampleRate
# t = arange(0,1,interval)
#
# ff=5
# y = np.sin(2*np.pi*ff*t)
#
# plt.subplot(2,1,1)
# plt.plot(t,y)
# plt.subplot(2,1,2)
# plotSpectrum(y, sampleRate)
# plt.show()