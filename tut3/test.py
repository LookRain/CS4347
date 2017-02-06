sample = [1,-1,5,6,7,8,1,-5,6,-5,7,-1]

zero_crosses = 0



num_buffers = 10
buffers = []

start = 0
end = 4
for i in range(num_buffers):
    buffer_data = sample[start:end]
    start += 2
    end += 2

    if len(buffer_data) == 4:
         buffers.append(buffer_data)


print(buffers)
print(len(buffers))