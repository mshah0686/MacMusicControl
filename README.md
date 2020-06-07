# MacMusicControl
Gesture recognition using Hexiwear, a wearable IOT device. Classify different wrist movements using sklearn machine learning models for music control. My music control keys on the keyboard are broken and it's annoying to change music through spotify app.

# Intro
My music control keys on my laptop broke so it's annoying to change music by changing apps while working.Instead, I wanted to build something cool instead.

Hexiwear is an IOT wearable device with a multitude of sensors and BLE suppurt. The project captures the XYZ acceleration, predicts gestures using sklearn libraries, and controls music with Apple OSA scripting.

# Data Gathering
First, the Data folder holds various CSV for different gestures and random noise. The three gestures are flicking your wrist right, left, and up. The random noise was used to train the model to prevent false positives and true negatives. Here are some XYZ acceleration graphs for different gestures showing that the gestures can be distinguished using the XYZ acceleration data (specifically the y axis for left and right and X axis for flick up).

![alt text](https://github.com/mshah0686/MacMusicControl/blob/master/Documentation/Left_down.png)
