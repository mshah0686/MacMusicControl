###########
# Author: Malav Shah
# ------------------
# Just used to plot things
############

import numpy as np
import matplotlib.pyplot as plt

data_left = np.genfromtxt('TrainingData/left_down.csv', delimiter=',')
data_right = np.genfromtxt('TrainingData/right_down.csv', delimiter=',')

plt.plot(data_left[:,1])

plt.plot(data_right[:,1])
plt.show()
