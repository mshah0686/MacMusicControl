###########
# Author: Malav Shah
# ------------------
# Read in x y z acceleration data from serial port
# Save data into a csv file
############

import matplotlib as plt
import serial
import numpy as np

def captureSerialData():
    port = _____

    sampleZise = 100000
    acc = np.zeros((sampleSize, 3), dtype = int)
    hexi = serial.Serial(port, 230400)
    hexi.flushInput()

    for i in range(sampleSize):
        data = hexi.readline()
        Data = data[:-2].split(b',')
        acc[i,0] = int(Data[0])
        acc[i,1] = int(Data[1])
        acc[i,2] = int(Data[2])

if __name__ == '__main__':
    accData = captureSerialData()
    np.saveText
    np.savetxt('trial1.csv', accData, delimiter=',', fmt='%d')




