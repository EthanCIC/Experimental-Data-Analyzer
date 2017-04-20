
# coding: utf-8

# In[1]:

import numpy as np
import matplotlib.pyplot as plt
import os
import re
import glob

# set exp. parameters
pumpPower = 0.014
measureTime = 30

# human sorting (Natrual sorting)
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [atoi(c) for c in re.split('(\d+)', text)]


# read files (sorted by natrual_keys) to a 3-D NumPy array
for files in sorted(glob.glob("*mV.csv"), key=natural_keys):
    print(files)
    try:
        dataTemp = np.genfromtxt(files, delimiter='\t')
        dataTemp = dataTemp[:, :, np.newaxis]
        data = np.concatenate((data, dataTemp), axis=2)
    except NameError:
        data = np.genfromtxt(files, delimiter='\t')
        data = data[:, :, np.newaxis]


# In[2]:

# Calculate biphotonRates, storing to NumPy array
biphotonRates = np.array([])

for i in range(np.shape(data)[2]):
    totalSum = np.sum(data[:,1, i])
    noiseAverage1024 = np.average(data[795:996,1, i])*1024
    areaOfPeak = totalSum - noiseAverage1024
    biphotonRate = areaOfPeak/pumpPower/measureTime
    biphotonRates = np.append(biphotonRates, biphotonRate)


# In[3]:

biphotonRates


# In[4]:

# Create x-axis data
x = np.array([])
for file in sorted(glob.glob("*mV.csv"), key=natural_keys):
    fileName = int(file.replace("mV.csv", ""))
    x = np.append(x, fileName)


# In[5]:

np.shape(biphotonRates)


# In[6]:

np.shape(x)


# In[7]:




# In[28]:

plt.plot(x, biphotonRates, 'o-')


# In[29]:

plt.show()


# In[26]:

from scipy.interpolate import interp1d
f = interp1d(x, biphotonRates, kind='cubic')
xnew = np.linspace(x.min(), x.max(), num=1000, endpoint=True)
plt.plot(xnew, f(xnew), '--', x, biphotonRates, 'bo')
plt.show()


# In[14]:

type(biphotonRates)


# In[ ]:



