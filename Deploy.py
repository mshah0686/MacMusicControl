###########
# Author: Malav Shah
# ------------------
# Train on gathered data and use model to output values on real time input
############
from Training import predict, train
from threading import Thread
import numpy as np
import scipy.signal as sig
import scipy.stats as stat
from threading import Event
from sklearn.ensemble import RandomForestClassifier
import serial
import time
import matplotlib as plt
import Music as controller

#create buffer full interupt event
buffer_full = Event()

#sample size
buffer_size = 80

#single samle
accX = np.zeros(buffer_size, dtype=float)
accY = np.zeros(buffer_size, dtype=float)
accZ = np.zeros(buffer_size, dtype=float)

buffer = np.zeros((buffer_size, 3))
samples_done = 0


def take_input():
    print('Started reading real time....')
    global accX, accY, accZ, buffer_size, samples_done, buffer
    port = '/dev/tty.usbmodem1422'
    input = serial.Serial(port,115200)
    input.flushInput()
    input.readline()
    while True:
        data = input.readline()
        new_sample = np.zeros((1, 3))
        new_sample = data[:-2].split(b',')
        #delete top element of buffer
        buffer = np.delete(buffer, 0, 0)
        #add new sample in (creates a queue)
        buffer = np.vstack((buffer, new_sample))
        samples_done = samples_done + 1
        if(samples_done == buffer_size):
            samples_done = 60
            buffer_full.set()

def analyze():
    global samples_done, buffer
    while True:
        buffer_full.wait(timeout=20)
        frame = np.array(buffer).astype(np.float)
        frame_var = np.var(frame, axis = 0)
        frame_skew = stat.skew(frame, axis = 0)
        frame_kurt = stat.kurtosis(frame, axis = 0)
        features = np.hstack((frame_var, frame_skew, frame_kurt))
        prediction = predict(features.reshape(1, -1))
        if(prediction[0] == 1):
            print('Gesture Detected: Left Down')
            controller.next()
            #if you detect a gester, clear buffer fully 
            #To prevent multiple detections on one gesture
            samples_done = 0
        elif(prediction[0] == 2):
            print('Gesture Detected: Right Down')
            controller.previous()
            samples_done = 0
        elif(prediction[0] == 3):
            print('Gesture Detected: Up Flick')
            controller.pause_play()
            samples_done = 0
        buffer_full.clear()

#init music
controller.init_music()

#train model
train()

#create serial input thread
thread_input = Thread(target=take_input)
thread_predict = Thread(target=analyze)
try:
    thread_input.start()
    thread_predict.start()
except Exception as e:
    print(e)

