# MacMusicControl
Gesture recognition using Hexiwear, a wearable IOT device. Classify different wrist movements using `sklearn` machine learning models for music control. My music control keys on the keyboard are broken and it's annoying to change music through spotify app.

# Intro
My music control keys on my laptop broke so it's annoying to change music by changing apps while working.Instead, I wanted to build something cool instead.

Hexiwear is an IOT wearable device with a multitude of sensors and BLE support. The project captures the XYZ acceleration, predicts gestures using `sklearn` libraries, and controls music with Apple OSA scripting.

# Data Gathering
The Hexiwear was programed to send XYZ data at 100Hz over serial (done in Python which is super cool for an embedded system.)

First, the Data folder holds various CSV for different gestures and random noise. The three gestures are flicking your wrist right, left, and up. The random noise was used to train the model to prevent false positives and true negatives. Here are some XYZ acceleration graphs for different gestures showing that the gestures can be distinguished using the XYZ acceleration data (specifically the y axis for left and right and X axis for flick up). The other gesture graphs are in the Documentation folder.

Left Down: You can see the peaks that occur on multiple gesture perfomances. The `Training.py` or `TrainSaveModel.py` script finds those peaks and uses them as frames as training data.
![alt text](https://github.com/mshah0686/MacMusicControl/blob/master/Documentation/Left_down.png)

Random Noise: A sliding frame was used to capture these as negative (no gestures)
![alt text](https://github.com/mshah0686/MacMusicControl/blob/master/Documentation/Noise.png)

# Training
Okay, at this point, I didn't know anything about machine learning. So I learned the theory on a Courseara Stanford Machine Learning course by Prof. Andrew Ng. Then, I learned about some learning libraries like `sklearn` and Tensorflow on Kaggle. I used `sklearn` for this project.

Variance, skew, and kurtosis I found were pretty accurate in distunguishing gestures. And, these three were calculated for a specific frame of time on the XYZ data (using peaks for the training Data).

# Deployment
As XYZ data comes into the serial port in realtime on one thread, a buffer implementation runs on another to predict a gesture when the buffer is full. Minor adjustments in calculating and storing buffer data was done to increase accuracy of the model. Then, once a gesture is predicted, the Apple OSA script controls the music.

The next step was to make it wireless. This is where I ran into trouble. I couldn't find a way to port the models and `sklearn` libraries into the Hexiwear device, so instead I opted for BLE communication from Hexiwear to the laptop. But then realized that my laptop doesn't support Bluetooth 4.1....dissapointing

# Further work
To make this work, I ordered a bluetooth dongle which is coming from China. In the meantime, I use it tethered to the laptop via usb cable. I found that it detects some false positives when the wrist moves back to flat position from either right or left because the acceleration data starts to look familiar to the opposite gesture. The solution I found was the empty the buffer fully for a few more samples after a gesture was detected so it ignores the next few milliseconds of data that would otherwise be detected as a false positive.

In terms of random noise, there were very few true negatives while usage. This is probably because the training was done on a full 90 degree wrist flick which you usually don't do while working on the laptop. And, I used random noise data in the training which helped reduce false positives.







