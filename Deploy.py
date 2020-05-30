###########
# Author: Malav Shah
# ------------------
# Train on gathered data and use model to output values on real time input
############
from Training import train
from threading import Thread
import numpy as np
from threading import Event
import serial
import time
import matplotlib.pyplot as plt

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
    print('Thread started')
    global sample, accX, accY, accZ, buffer_size, samples_done, buffer
    port = '/dev/tty.usbmodem1422'
    input = serial.Serial(port,115200)
    input.flushInput()
    input.readline()
    while True:
        while True:
            data = input.readline()
            new_sample = np.zeros((1, 3))
            new_sample = data[:-2].split(b',')
            #delete top element of buffer
            buffer = np.delete(buffer, 0, 0)
            #new_sample = np.zeros((1, 3))
            #new_sample[0] = float(data[0])
            #new_sample[1] = float(data[1])
            #new_sample[2] = float(data[2])
            #append new sample at the end
            buffer = np.vstack((buffer, new_sample))
            samples_done = samples_done + 1
            if(samples_done == buffer_size):
                print('Buffer full')
                buffer_full.set()
                samples_done = 60

def analyze():
    global samples_done, buffer
    while True:
        buffer_full.wait(timeout = 20)
        print('Event called')
        buffer_full.clear()

#get model
#create serial input thread
thread_input = Thread(target=take_input)
thread_predict = Thread(target=analyze)
try:
    thread_input.start()
    thread_predict.start()
except Exception as e:
    print(e)

