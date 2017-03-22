import numpy as np
import scipy.io.wavfile
import scipy.signal
import matplotlib.pyplot as plt

SAMPLING_RATE = 44100
SAMPLING_SIZE1 = 16384
FREQ_1 = 100.0
FREQ_2 = 1234.56
SAMPLING_SIZE2 = 2048
DURATION = 1.0
AMPLITUDE = 1.0


def main():
    #generate the 2 perfect sine waves with different frequency
    freq_1_perfect_sin = perpect_sin(FREQ_1)
    freq_2_perfect_sin = perpect_sin(FREQ_2)

    #generate the 8 waves
    freq_1_size_1_no_interpolation = no_interpolation(FREQ_1, SAMPLING_SIZE1)
    freq_1_size_2_no_interpolation = no_interpolation(FREQ_1, SAMPLING_SIZE2)

    freq_2_size_1_no_interpolation = no_interpolation(FREQ_2, SAMPLING_SIZE1)
    freq_2_size_2_no_interpolation = no_interpolation(FREQ_2, SAMPLING_SIZE2)

    freq_1_size_1_linear_interpolation = linear_interpolation(FREQ_1, SAMPLING_SIZE1)
    freq_1_size_2_linear_interpolation = linear_interpolation(FREQ_1, SAMPLING_SIZE2)

    freq_2_size_1_linear_interpolation = linear_interpolation(FREQ_2, SAMPLING_SIZE1)
    freq_2_size_2_linear_interpolation = linear_interpolation(FREQ_2, SAMPLING_SIZE2)

    #calculate the max errors and write them to file
    max_error1 = 32767 * np.max(np.abs(freq_1_size_1_no_interpolation - freq_1_perfect_sin[:SAMPLING_SIZE1]))
    max_error2 = 32767 * np.max(np.abs(freq_1_size_2_no_interpolation - freq_1_perfect_sin[:SAMPLING_SIZE2]))
    max_error3 = 32767 * np.max(np.abs(freq_1_size_1_linear_interpolation - freq_1_perfect_sin[:SAMPLING_SIZE1]))
    max_error4 = 32767 * np.max(np.abs(freq_1_size_2_linear_interpolation - freq_1_perfect_sin[:SAMPLING_SIZE2]))
    max_error5 = 32767 * np.max(np.abs(freq_2_size_1_no_interpolation - freq_2_perfect_sin[:SAMPLING_SIZE1]))
    max_error6 = 32767 * np.max(np.abs(freq_2_size_2_no_interpolation - freq_2_perfect_sin[:SAMPLING_SIZE2]))
    max_error7 = 32767 * np.max(np.abs(freq_2_size_1_linear_interpolation - freq_2_perfect_sin[:SAMPLING_SIZE1]))
    max_error8 = 32767 * np.max(np.abs(freq_2_size_2_linear_interpolation - freq_2_perfect_sin[:SAMPLING_SIZE2]))

    write_error("max_audio_file_error.txt",max_error1,max_error2,max_error3,max_error4,max_error5,max_error6,max_error7,max_error8)


#generate lut table
def LUT(size):
    array = np.arange(size)
    lut = np.sin(2.0 * np.pi * array / size)

    return lut


#generate sine without interpolation
def no_interpolation(freq, size):
    buffer = np.zeros(size)
    lut = LUT(size)
    diff = freq / SAMPLING_RATE * size
    for i in range(size):
        buffer[i] = lut[round(i * diff) % size]
    return buffer


#generate sine with linear interpolation
def linear_interpolation(freq, size):
    buffer = np.zeros(size)
    lut = LUT(size)
    diff = freq / SAMPLING_RATE * size
    for i in range(size):
        x0 = np.floor(i * diff % size)
        x1 = x0 + 1
        y0 = lut[x0 % size]
        y1 = lut[x1 % size]
        buffer[i] = y0 + (y1 - y0) * ((i * diff % size) - x0) / (x1 - x0)
    return buffer


#generate perfect sine wave
def perpect_sin(freq):
    period = np.arange(int(DURATION * SAMPLING_RATE))
    sin_wave = AMPLITUDE * np.sin(2.0 * np.pi * (freq / SAMPLING_RATE) * period)
    return sin_wave


def write_error(name,e1,e2,e3,e4,e5,e6,e7,e8):
    f = open(name, "w")
    f.write('Frequency\tInterpolation\t16384-sample\t\t2048-sample\n')
    f.write('100Hz\t\tNo\t\t%s\t\t%s\n' % (str(e1), str(e2)))
    f.write('\t\tLinear\t\t%s\t%s\n' % (str(e3), str(e4)))
    f.write('1234.56Hz\tNo\t\t%s\t\t%s\n' % (str(e5), str(e6)))
    f.write('\t\tLinear\t\t%s\t%s\n' % (str(e7), str(e8)))


main()