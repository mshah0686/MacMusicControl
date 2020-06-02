###########
# Author: Malav Shah
# ------------------
# Just used to plot things
############

import numpy as np
import matplotlib.pyplot as plt

data_left = np.genfromtxt('TrainingData/left_down.csv', delimiter=',')
data_right = np.genfromtxt('TrainingData/right_down.csv', delimiter=',')
noise = np.genfromtxt('TrainingData/random_noise.csv', delimiter = ',')

#plt.plot(data_left)
#plt.plot(data_right)
plt.plot(noise)
plt.show()
