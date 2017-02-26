from scipy.io import wavfile
import numpy as np
import scipy.signal
import scipy.fftpack
import math
import matplotlib.pyplot as plt

buffer_length = 1024


def main():
    mfFilename = "../music_speech.mf"
    music_speech_file = open(mfFilename)
    music_speech_file.close()

    # read mf file and all wav files, initialize the arff file headers
    write_header()

    # initialise mel filters
    filters = np.zeros((26, 512 + 1))

    # read wav files one by one, calculating their features
    with open(mfFilename, 'r') as file:
        for line in file:
            splitString = line.split('\t')
            type = splitString[1].strip()  # array of file type
            path = "../music_speech/" + splitString[0]
            rate, data = wavfile.read(path)

            # Since the sound pressure values have int16 datatype, we divide the values by 2^15 to convert them to
            # float values ranging from -1 to 1
            sample = data / 32768.0
            sample = np.array(sample)
            length = np.size(sample)


            # # initialize buffers
            num_buffers = int(length/buffer_length) * 2
            buffers = []
            start = 0
            end = buffer_length
            fftMatrix = np.zeros((1290, 1024 / 2 + 1))
            bufferMatrix = np.zeros((num_buffers, buffer_length))
            # generate buffers with hopsize of 512 ignoring incomplete buffers
            for i in range(num_buffers):
                buffer_data = sample[start:end]

                start += 512
                end += 512
                bufferMatrix[i, :] = buffer_data


            # applying pre-emphasis filter and hamming windowing
            bufferMatrix = pre_emphasize(bufferMatrix)
            bufferMatrix = bufferMatrix * scipy.signal.hamming(buffer_length)
            bufferMatrix = mag_spec(bufferMatrix)

            mel = freq_to_mel(rate)



            for j in range(26):
                # left, top, right = calFilters(j, mel, rate / 1024.0)

                left = mel_to_freq(mel * j) / (rate / buffer_length)
                top = mel_to_freq(mel * (j + 1)) / (rate / buffer_length)
                right = mel_to_freq(mel * (j + 2)) / (rate / buffer_length)

                #
                left = math.floor(left)
                top = round(top)
                right = math.ceil(right)

                left_point_arr = np.linspace(0, 1, top - left + 1)
                left_point_arr = np.delete(left_point_arr, -1)
                right_point_arr = np.linspace(1, 0, right - top + 1)
                left_bin = np.zeros(left)
                mel_points = np.concatenate((left_bin, left_point_arr, right_point_arr))
                filters[j] = np.concatenate((mel_points, np.zeros(512.0 - right)))

            filters_transposed = filters.T
            mfcc_matrix = mfcc(bufferMatrix, filters_transposed)

            write_mean_sd_type(mfcc_matrix, type)
    plot_fig1(filters, rate)
    plot_fig2(filters, rate)


def plot_fig1(filters, rate):
    freq = np.linspace(0, rate / 2, 512+1)
    fig = plt.figure()
    for i in range(26):
        plt.plot(freq, filters[i])

    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.title("26 Triangular MFCC filters, 22050 Hz signal, window size 1024")
    plt.savefig("graph 1")


def plot_fig2(filters, rate):
    freq = np.linspace(0, rate / 2, 512+1)
    fig = plt.figure()
    for i in range(26):
        plt.plot(freq, filters[i])

    plt.xlim(0, 300)

    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.title("26 Triangular MFCC filters, 22050 Hz signal, window size 1024")
    plt.savefig("graph 2")


def mfcc(buffer, filters):
    result = np.dot(buffer, filters)
    result = np.log10(result)
    result = scipy.fftpack.dct(result)
    return result


def pre_emphasize(matrix):
    shifted_matrix = np.zeros([1290, buffer_length])
    shifted_matrix[:, 1:buffer_length] = matrix[:, :-1]
    result = matrix - (0.95 * shifted_matrix)
    return result


def mag_spec(matrix):
    fft = scipy.fftpack.fft(matrix, axis = 1)
    mag_spectrum = np.abs(fft[:, 0:buffer_length / 2 + 1])
    return mag_spectrum


def freq_to_mel(frequency):
    result = 1127 * np.log(1 + (frequency / 2.0) / 700) / (26 + 1)
    return result


def mel_to_freq(mel):
    result = (np.exp(mel / 1127) - 1) * 700.0
    return result


def write_header():
    ans_path = "assignment3.arff"
    ans_file = open(ans_path, 'w')
    ans_file.write("@RELATION music_speech\n")
    for i in range(26):
        ans_file.write("@ATTRIBUTE MFCC_MEAN_%d NUMERIC\n" % (i))
    for j in range(26):
        ans_file.write("@ATTRIBUTE MFCC_STD_%d NUMERIC\n" % (j))
    ans_file.write( "@ATTRIBUTE class {music,speech}\n\n@DATA\n")


def write_mean_sd_type(featureMatrix, type):
    ans_path = "assignment3.arff"
    ans_file = open(ans_path, "a")

    mean = np.mean(featureMatrix, 0)
    standard = np.std(featureMatrix, 0)
    MEANstring = np.char.mod('%f', mean)
    MEANstring = ",".join(MEANstring)
    STDstring = np.char.mod('%f', standard)
    STDstring = ",".join(STDstring)

    ans_file.write("%s,%s,%s" % (MEANstring, STDstring, type))
    ans_file.write("\n")

main()
