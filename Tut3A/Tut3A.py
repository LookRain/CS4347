import wave
import numpy as np
import sys
import numpy
from scipy.io import wavfile
import numpy as np
import csv


def main():
    mfFilename = "music_speech.mf"
    # mf = open("music_speed.mf", "r", 0)
    types = []
    paths = []
    datas = []
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






            # if count == 1:
            #     print(data.shape)
            #     print(processed_data)
            #     print(processed_data.__sizeof__())
            #     count += 1

                #     paths.append(path)
                #     types.append(type)
                #     datas.append(data)
                #
                # print(types)
                # print(types.__len__())
                # print(paths)
                # print(paths.__len__())
                # print(datas.__len__())

def calRMS(sample):
    # 1(a)
    # Calculating RMS using numpy
    rms = np.sqrt(np.mean(sample ** 2))
    return rms
def calPAR(sample, rms):
    # 1(b)
    # Calculating PAR
    par = np.amax(abs(sample)) / rms
    # print(par)
    return par
def calZCR(sample):

    # 1(c)
    # Calculating Zero-Crossing Rate
    # The following commented code is the orginal solution, but the current one seems to work much faster
    # zero_crosses = 0
    # for i in range(len(sample) - 1):
    #     if sample[i] * sample[i + 1] < 0:
    #         zero_crosses += 1
    zc = ((sample[:-1] * sample[1:]) < 0).sum()
    zcr = zc / len(sample)
    # print(zcr)
    return zcr

def calMAD(sample):
    # 1(d)
    # Calculating MAD
    sample_median = np.median(sample)

    mad = np.median(abs(sample - sample_median))
    # print(mad)
    return mad
def calMeanAD(sample):
    # 1(e)
    # Calculating MEAN-AD
    sample_mean = np.mean(sample)
    mean_ad = np.mean(abs(sample - sample_mean))
    # print(mean_ad)
    return mean_ad

main()