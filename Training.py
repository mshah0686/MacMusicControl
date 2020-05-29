###########
# Author: Malav Shah
# ------------------
# Train data on gathered truth data using RandomForrestClassifier
############

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig
import scipy.stats as stat
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix

left_movement = np.genfromtxt('truthPositives.csv', delimiter=',')
noise = np.genfromtxt('randomNoise.csv', delimiter = ',')
#xyz -> 0 1 2
#peaks,_ = sig.find_peaks(left_movement[:,1], height = 7.5)
#plt.figure(num=1)
#plt.plot(left_movement[:,1])
#plt.figure(num = 1)
#plt.plot(peaks, left_movement[peaks,1], 'x')
#plt.show()


total_features = []

def extract_features():
    total_features = []
    print('Extracting features')
    peaks,_ = sig.find_peaks(left_movement[:,1], height = 7.5)
    for peak in peaks:
        #f is the sub frame of the peak (certain parameter left and right of it)
        frame = left_movement[peak-30:peak+45, :]
        frame_var = np.var(frame, axis = 0)
        frame_skew = stat.skew(frame, axis = 0)
        frame_kurt = stat.kurtosis(frame, axis = 0)

        features = np.hstack((frame_var, frame_skew, frame_kurt))
        if np.size(total_features) == 0:
            total_features = features
        else:
            total_features = np.vstack((total_features, features))
    #classify positive as 1
    y = np.ones(len(peaks))
    return total_features, y

def extract_noise():
    total_features = []
    size = len(noise[:,2])
    samples_done = 0
    for i in range(40, size - 45, 25):
        samples_done = samples_done + 1
        frame = noise[i - 35: i+45, :]
        frame_var = np.var(frame, axis = 0)
        frame_skew = stat.skew(frame, axis = 0)
        frame_kurt = stat.kurtosis(frame, axis = 0)

        features = np.hstack((frame_var, frame_skew, frame_kurt))
        if np.size(total_features) == 0:
            total_features = features
        else:
            total_features = np.vstack((total_features, features))
    y = np.zeros(samples_done)
    return total_features, y


def train_model(X, y):
   #ideally shuffle data here, but only one classifier so it is okay

   model = RandomForestClassifier(n_estimators=20)
   cross_val_scores = cross_val_score(model, X, y, cv = 3)
   print(cross_val_scores)

   model.fit(X, y)
   return model



if __name__ == '__main__':
    print('Entering training.....')
    total_features_pos, y_pos = extract_features()
    total_features_neg, y_neg = extract_noise()
    #combine data
    y = np.append(y_pos, y_neg)
    X = np.vstack((total_features_pos, total_features_neg))
    #randomize data
    data = np.hstack((X, np.reshape(y, (-1,1))))
    np.random.shuffle(data)
    y = data[:,-1]
    X = data[:, :-1]

    #train model
    trained_model = train_model(X,y)
    
    #predict model
    predictions = trained_model.predict(X)
    print(confusion_matrix(y, predictions))




