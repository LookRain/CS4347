from scipy.io import wavfile
import numpy as np
import scipy.signal
import scipy.fftpack

buffer_length = 1024


def main():
    mfFilename = "music_speech.mf"
    music_speech_file = open(mfFilename)
    music_speech_file.close()

    # read mf file and all wav files, initialize the arff file headers
    writeHeader()


    # read wav files one by one, calculating their features
    with open(mfFilename, 'r') as file:
        for line in file:
            splitString = line.split('\t')
            type = splitString[1].strip()  # array of file type
            path = splitString[0]
            rate, data = wavfile.read(path)

            # Since the sound pressure values have int16 datatype, we divide the values by 2^15 to convert them to
            # float values ranging from -1 to 1
            sample = data / 32768.0
            sample = np.array(sample)
            length = np.size(sample)
            # initialize buffers
            num_buffers = int(length/buffer_length) * 2
            buffers = []
            start = 0
            end = buffer_length
            fftMatrix = np.zeros((1290, 1024 / 2 + 1))
            # generate buffers with hopsize of 512 ignoring incomplete buffers
            for i in range(num_buffers):
                buffer_data = sample[start:end]
                buffer_data = buffer_data * scipy.signal.hamming(buffer_length)
                bufferFFT = scipy.fftpack.fft(buffer_data)
                bufferFFT = bufferFFT[:buffer_length / 2 + 1]
                bufferFFT = np.abs(bufferFFT)
                fftMatrix[i, :] = bufferFFT

                start += 512
                end += 512

            featureMatrix = np.zeros((num_buffers, 5))
            featureMatrix[:, 0] = calcSC(fftMatrix)
            featureMatrix[:, 1] = np.apply_along_axis(calcSRO, 1, fftMatrix)
            featureMatrix[:, 2] = calcSFM(fftMatrix)
            featureMatrix[:, 3] = calcPARFFT(fftMatrix)
            featureMatrix[:, 4] = calcFLUX(fftMatrix)

            writeData(featureMatrix, type)


def calcSC(matrix):
    SCMatrix = np.copy(matrix)
    grid = np.indices((1290, 513))
    SC = np.sum(grid[1] * SCMatrix, axis=1) / np.sum(SCMatrix, axis=1)
    return SC


def calcSRO(matrix):
    SROMatrix = np.copy(matrix)
    SROcompare = 0.85 * np.sum(SROMatrix)
    SROsum = 0

    for i in range(0, len(SROMatrix)):
        SROsum += SROMatrix[i]
        if SROsum >= SROcompare:
            return i


def calcSFM(matrix):
    gMean = np.exp(np.mean(np.log(matrix), axis=1))
    aMean = np.mean(matrix, axis=1)
    SFM = gMean / aMean
    return SFM


def calcPARFFT(matrix):
    RMS = np.sqrt(np.mean(np.square(matrix), axis=1))
    PAR = np.amax(matrix, axis=1)
    PARFFT = PAR / RMS
    return PARFFT


def calcFLUX(matrix):
    SFMatrix = np.copy(matrix)
    minusOne = np.zeros(matrix.shape[1])
    SFprev = np.vstack([minusOne, matrix[:-1]])
    SFdiff = SFMatrix - SFprev
    SF = np.sum(SFdiff.clip(0), axis=1)
    return SF


def writeHeader():
    ans_path = "assignment2.arff"
    ans_file = open(ans_path, 'w')
    ans_file.write('''@RELATION music_speech
@ATTRIBUTE SC_MEAN NUMERIC
@ATTRIBUTE SRO_MEAN NUMERIC
@ATTRIBUTE SFM_MEAN NUMERIC
@ATTRIBUTE PARFFT_MEAN NUMERIC
@ATTRIBUTE FLUX_MEAN NUMERIC
@ATTRIBUTE SC_STD NUMERIC
@ATTRIBUTE SRO_STD NUMERIC
@ATTRIBUTE SFM_STD NUMERIC
@ATTRIBUTE PARFFT_STD NUMERIC
@ATTRIBUTE FLUX_STD NUMERIC
@ATTRIBUTE class {music,speech}\n\n@DATA\n''')


def writeData(featureMatrix, type):
    ans_path = "assignment2.arff"
    ans_file = open(ans_path, "a")
    ans_matrix = np.zeros(10)
    ans_matrix[0:5] = np.mean(featureMatrix, axis=0)
    ans_matrix[5:10] = np.std(featureMatrix, axis=0)
    SC_MEAN = ans_matrix[0]
    SRO_MEAN = ans_matrix[1]
    SFM_MEAN = ans_matrix[2]
    PARFFT_MEAN = ans_matrix[3]
    FLUX_MEAN = ans_matrix[4]
    SC_STD = ans_matrix[5]
    SRO_STD = ans_matrix[6]
    SFM_STD = ans_matrix[7]
    PARFFT_STD = ans_matrix[8]
    FLUX_STD = ans_matrix[9]

    ans_file.write("%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%s\n" % (SC_MEAN, SRO_MEAN, SFM_MEAN, PARFFT_MEAN, FLUX_MEAN, SC_STD, SRO_STD, SFM_STD, PARFFT_STD, FLUX_STD, type))


main()
