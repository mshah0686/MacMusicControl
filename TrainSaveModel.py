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
import pickle

noise = np.genfromtxt('randomNoise.csv', delimiter = ',')
#xyz -> 0 1 2
#peaks,_ = sig.find_peaks(left_movement[:,1], height = 7.5)
#plt.figure(num=1)
#plt.plot(left_movement[:,1])
#plt.figure(num = 1)
#plt.plot(peaks, left_movement[peaks,1], 'x')
#plt.show()


total_features = []

def extract_features(file_name):
    left_movement = np.genfromtxt(file_name, delimiter=',')
    total_features = []
    print('Extracting features...')
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
   model = RandomForestClassifier(n_estimators=20)
   cross_val_scores = cross_val_score(model, X, y, cv = 3)
   print(cross_val_scores)

   model.fit(X, y)
   return model

trained_model = RandomForestClassifier()

#Extract features and return a trained model
if __name__ == '__main__':
    print('Entering training.....')
    #extract features from two csv files
    total_features_pos, y_pos = extract_features('training_set.csv')
    total_features_neg, y_neg = extract_noise()

    #combine data
    y = np.append(y_pos, y_neg)
    X = np.vstack((total_features_pos, total_features_neg))
    #randomize data
    print('Pre-proc: getting training features...')
    data = np.hstack((X, np.reshape(y, (-1,1))))
    np.random.shuffle(data)
    y = data[:,-1]
    X = data[:, :-1]

    #train model
    print('Training model...')
    trained_model = train_model(X,y)

    #Save model as file
    print('saving model...')
    filename = 'finalized_model.sav'
    pickle.dump(trained_model, open(filename, 'wb'))

    #create validation set data
    print('cross validating...')
    cv_x, cv_y = extract_features('cv_set.csv')
    cv_x = np.vstack((cv_x, total_features_neg))
    cv_y = np.append(cv_y, y_neg)
    
    #Validate on model
    print('Validation scores....on model loaded from file')
    loaded_model = pickle.load(open(filename, 'rb'))
    predictions = loaded_model.predict(cv_x)
    print('CV SCORES: '),
    print(confusion_matrix(cv_y, predictions))
    print('Finished training....')


