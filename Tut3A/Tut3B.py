import wave
import numpy as np
import sys
import numpy
from scipy.io import wavfile
import numpy as np
import csv


def main():
    mfFilename = "music_speech.mf"
    ans = "ans2.arff"
    ans_file = open(ans, "w")
    with open(mfFilename, 'r') as file:
        count = 1
        for line in file:
            splitString = line.split('\t')
            type = splitString[1].strip()  # array of file type
            short_path = splitString[0]
            path = 'music_speech/' + short_path  # array of file path

            freq, data = wavfile.read(path)
            # Since the sound pressure values have int16 datatype, we divide the values by 2^15 to convert them to
            # float values ranging from -1 to 1
            sample = data / 32768.0
            num_buffers = 1290
            buffers = []
            # print(sample)
            start = 0
            end = 1024
            for i in range(num_buffers):
                buffer_data = sample[start:end]
                start += 512
                end += 512

                buffers.append(buffer_data)
            # print(len(buffers))
            # print(buffers)
            # print(len(buffers[1289]))
            # print(len(sample))

            rms_array = []
            par_array = []
            zcr_array = []
            mad_array = []
            meanan_array = []
            for i in range(len(buffers)):

                rms = calRMS(buffers[i])
                par = calPAR(buffers[i], rms)
                zcr = calZCR(buffers[i])
                mad = calMAD(buffers[i])
                meanad = calMeanAD(buffers[i])
                rms_array.append(rms)
                par_array.append(par)
                zcr_array.append(zcr)
                mad_array.append(mad)
                meanan_array.append(meanad)

                # print('%.6f' % rms_mean + ',' + '%.6f' % par_mean + ',' + '%.6f' % zcr_mean + ',' + '%.6f' % mad_mean + ',' + '%.6f' % meanad_mean + '\n')
            # print(np.mean(rms_array))
            rms_mean = np.mean(rms_array)
            par_mean = np.mean(par_array)
            zcr_mean = np.mean(zcr_array)
            mad_mean = np.mean(mad_array)
            meanad_mean = np.mean(meanan_array)

            rms_std = np.std(rms_array)
            par_std = np.std(par_array)
            zcr_std = np.std(zcr_array)
            mad_std = np.std(mad_array)
            meanad_std = np.std(meanan_array)
            print( '%.6f' % rms_mean + ',' + '%.6f' % par_mean + ',' + '%.6f' % zcr_mean + ',' + '%.6f' % mad_mean + ',' + '%.6f' % meanad_mean +  '%.6f' % rms_std + ',' + '%.6f' % par_std + ',' + '%.6f' % zcr_std + ',' + '%.6f' % mad_std + ',' + '%.6f' % meanad_std + ',' + type)
            ans_file.write( '%.6f' % rms_mean + ',' + '%.6f' % par_mean + ',' + '%.6f' % zcr_mean + ',' + '%.6f' % mad_mean + ',' + '%.6f' % meanad_mean +  '%.6f' % rms_std + ',' + '%.6f' % par_std + ',' + '%.6f' % zcr_std + ',' + '%.6f' % mad_std + ',' + '%.6f' % meanad_std + ',' + type + '\n')
            # rms = calRMS(sample)
            # par = calPAR(sample, rms)
            # zcr = calZCR(sample)
            # mad = calMAD(sample)
            # meanad = calMeanAD(sample)
            # ans_file.write(short_path + ',' + '%.6f' % rms + ',' + '%.6f' % par + ',' + '%.6f' % zcr + ',' + '%.6f' % mad + ',' + '%.6f' % meanad + '\n')


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
    # The following commented code is the original solution, but the current one seems to work much faster
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
