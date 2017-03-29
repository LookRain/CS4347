import arff
import numpy as np
import pprint
import matplotlib.pyplot as plt

file = open('time-domain.arff')
obj = arff.loads(file)
list = obj['data']
PAR_MEAN_m = []
PAR_MEAN_s = []
ZCR_MEAN_m = []
ZCR_MEAN_s = []
PAR_STD_m = []
PAR_STD_s = []
ZCR_STD_m = []
ZCR_STD_s = []
TYPE=[]
for row in list:
    if (row[10] == "music"):
        PAR_MEAN_m.append(row[1])
        ZCR_MEAN_m.append(row[2])

        PAR_STD_m.append(row[6])
        ZCR_STD_m.append(row[7])
    else:
        PAR_MEAN_s.append(row[1])
        ZCR_MEAN_s.append(row[2])

        PAR_STD_s.append(row[6])
        ZCR_STD_s.append(row[7])
    TYPE.append(row[10])
print(TYPE)

plt.plot(ZCR_MEAN_m, PAR_MEAN_m, 'bo', label='Music')
plt.plot(ZCR_MEAN_s, PAR_MEAN_s, 'ro', label='Speech')
plt.xlabel('ZCR mean')
plt.ylabel('PAR mean')
plt.legend()
plt.show()

plt.plot(ZCR_STD_m, PAR_STD_m, 'go', label='Music')
plt.plot(ZCR_STD_s, PAR_STD_s, 'yo', label='Speech')
plt.xlabel('ZCR std')
plt.ylabel('PAR std')
plt.legend()
plt.show()

# print(PAR_MEAN)
# print(ZCR_MEAN)
# print(PAR_STD)
# print(ZCR_STD)
