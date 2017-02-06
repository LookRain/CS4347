sample = [1,-1,5,6,7,8,1,-5,6,-5,7,-1]

zero_crosses = 0
for i in range(len(sample) - 1):

    if sample[i] * sample[i + 1] < 0:

        zero_crosses += 1


print(zero_crosses)