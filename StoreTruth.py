###########
# Author: Malav Shah
# ------------------
# Read in x y z acceleration data from serial port
# Save data into a csv file
############

import matplotlib.pyplot as plt
import serial
import numpy as np

def captureSerialData():
    sample_rate = 100 #hertz
    time = 10 #seconds
    sampleSize = sample_rate * time

    port = '/dev/tty.usbmodem1422'
    acc = np.zeros((sampleSize, 3), dtype = float)
    hexi = serial.Serial(port,115200)
    hexi.flushInput()
    print('Starting capture')
    try:
        print('inside try')
        for i in range(sampleSize):
            data = hexi.readline()
            Data = data[:-2].split(b',')
            print(Data)
            acc[i,0] = float(Data[0])
            acc[i,1] = float(Data[1])
            acc[i,2] = float(Data[2])
            print(sampleSize - i)
        return acc
        hexi.close()
    except Exception as e:
        print(e)
        print("exception")
        return acc

if __name__ == '__main__':
    accData = captureSerialData()
    plt.plot(accData)
    np.savetxt('flik_up.csv', accData, delimiter=',', fmt='%d')
    plt.show()





