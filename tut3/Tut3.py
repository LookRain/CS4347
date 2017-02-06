import wave
import numpy as np
import sys
from scipy.io import wavfile


def readTruthData():
    mfFilename = "./music_speech.mf.txt"
     # mf = open("music_speed.mf", "r", 0)
    types = []
    paths = []
    datas = []
    with open(mfFilename, 'r') as file:
        count = 1
        for line in file:
            splitString = line.split('\t')
            type = splitString[1].strip() # array of file type
            path = 'music_speech/' + splitString[0] # array of file path

            rate, data = wavfile.read(path)


            processed_data = data / 32768.0
            if count == 1:

                print(processed_data)
                print(processed_data.__sizeof__())
                count += 1





           
        #     paths.append(path)
        #     types.append(type)
        #     datas.append(data)
        #
        # print(types)
        # print(types.__len__())
        # print(paths)
        # print(paths.__len__())
        # print(datas.__len__())
readTruthData()