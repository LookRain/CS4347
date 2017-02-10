from scipy.io import wavfile
import numpy as np


def main():
    # read mf file and all wav files, initialize the arff file headers
    mfFilename = "music_speech.mf"
    ans = "ans2.arff"
    ans_file = open(ans, "w")
    header = '@RELATION music_speech\n@ATTRIBUTE RMS_MEAN NUMERIC\n@ATTRIBUTE PAR_MEAN NUMERIC\n@ATTRIBUTE ZCR_MEAN NUMERIC\n@ATTRIBUTE MAD_MEAN NUMERIC\n@ATTRIBUTE MEAN_AD_MEAN NUMERIC\n@ATTRIBUTE RMS_STD NUMERIC\n@ATTRIBUTE PAR_STD NUMERIC\n@ATTRIBUTE ZCR_STD NUMERIC\n@ATTRIBUTE MAD_STD NUMERIC\n@ATTRIBUTE MEAN_AD_STD NUMERIC\n@ATTRIBUTE class {music,speech}\n\n'
    ans_file.write(header + '@DATA\n')

    # read wav files one by one, calculating their features
    with open(mfFilename, 'r') as file:
        for line in file:
            splitString = line.split('\t')
            type = splitString[1].strip()  # array of file type
            short_path = splitString[0]
            path = 'music_speech/' + short_path  # array of file path

            freq, data = wavfile.read(path)
            # Since the sound pressure values have int16 datatype, we divide the values by 2^15 to convert them to
            # float values ranging from -1 to 1
            sample = data / 32768.0

            # initialize buffers
            num_buffers = 1290
            buffers = []
            start = 0
            end = 1024
            # generate buffers with hopsize of 512 ignoring incomplete buffers
            for i in range(num_buffers):
                buffer_data = sample[start:end]
                start += 512
                end += 512

                if len(buffer_data) == 1024:
                    buffers.append(buffer_data)

            # initialize arrays for all features
            rms_array = []
            par_array = []
            zcr_array = []
            mad_array = []
            meanan_array = []

            # calculate features
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
            # genereate mean and std of features, write to answer file
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
            print('%.6f' % rms_mean + ',' + '%.6f' % par_mean + ',' + '%.6f' % zcr_mean + ',' + '%.6f' % mad_mean + ',' + '%.6f' % meanad_mean + ',' + '%.6f' % rms_std + ',' + '%.6f' % par_std + ',' + '%.6f' % zcr_std + ',' + '%.6f' % mad_std + ',' + '%.6f' % meanad_std + ',' + type)
            ans_file.write('%.6f' % rms_mean + ',' + '%.6f' % par_mean + ',' + '%.6f' % zcr_mean + ',' + '%.6f' % mad_mean + ',' + '%.6f' % meanad_mean + ',' + '%.6f' % rms_std + ',' + '%.6f' % par_std + ',' + '%.6f' % zcr_std + ',' + '%.6f' % mad_std + ',' + '%.6f' % meanad_std + ',' + type + '\n')


def calRMS(sample):    # Calculating RMS using numpy
    rms = np.sqrt(np.mean(sample ** 2))
    return rms


def calPAR(sample, rms):  # Calculating PAR
    par = np.amax(abs(sample)) / rms
    return par


def calZCR(sample):   # Calculating Zero-Crossing Rate
    zc = ((sample[:-1] * sample[1:]) < 0).sum()
    zcr = zc / (len(sample) - 1)
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
