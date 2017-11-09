import numpy as np

array= np.zeros((100,200))

for row in range(100):
    for column in range(200):
        array[row,column]=row*1000+column

print(array[10,20])
print(array[20,30])
print(array[40,10])

print(np.average(array,axis=1))
print(np.average(array,axis=0))

an_array = np.array([i for i in range(0,10)])

print(np.concatenate((an_array[:9], an_array[9+1:])))

print([i for i in range(10) if i!=5])

