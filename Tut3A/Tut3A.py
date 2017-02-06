import wave
import numpy as np
import sys
import numpy
from scipy.io import wavfile
import numpy as np
import csv


def main():
    mfFilename = "music_speech.mf"
    ans = "ans.csv"
    ans_file = open(ans, "w")
    with open(mfFilename, 'r') as file:
        count = 1
        for line in file:
            splitString = line.split('\t')
            type = splitString[1].strip()  # array of file type
            short_path = splitString[0]
            path = 'music_speech/' + short_path  # array of file path

            freq, data = wavfile.read(path)
            # Since the sound pressure values are int16 types, we divide the values by 2^15 to convert them to
            # float values ranging from -1 to 1
            sample = data / 32768.0

            rms = calRMS(sample)
            par = calPAR(sample, rms)
            zcr = calZCR(sample)
            mad = calMAD(sample)
            meanad = calMeanAD(sample)
            ans_file.write(short_path + ',' + '%.6f' % rms + ',' + '%.6f' % par + ',' + '%.6f' % zcr + ',' + '%.6f' % mad + ',' + '%.6f' % meanad + '\n')


def calRMS(sample):    # Calculating RMS using numpy
    rms = np.sqrt(np.mean(sample ** 2))
    return rms


def calPAR(sample, rms):  # Calculating PAR
    par = np.amax(abs(sample)) / rms
    return par


def calZCR(sample):   # Calculating Zero-Crossing Rate
    zc = ((sample[:-1] * sample[1:]) < 0).sum()
    zcr = zc / len(sample)
    return zcr


def calMAD(sample):  # Calculating MAD
    sample_median = np.median(sample)

    mad = np.median(abs(sample - sample_median))
    return mad


def calMeanAD(sample):    # Calculating MEAN-AD
    sample_mean = np.mean(sample)
    mean_ad = np.mean(abs(sample - sample_mean))
    return mean_ad


main()
