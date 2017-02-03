import wave
import numpy as np
import sys


def readTruthData():
    mfFilename = "./music_speech.mf.txt"
     # mf = open("music_speed.mf", "r", 0)
    types = []
    paths = []
    with open(mfFilename, 'r') as file:
        for line in file:
            splitString = line.split('\t')
            type = splitString[1].strip()
            path = splitString[0]


           
            paths.append(path)
            types.append(type)


        print(types)
        print(paths)
readTruthData()