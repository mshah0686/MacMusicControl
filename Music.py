###########
# Author: Malav Shah
# ------------------
# Train data on gathered truth data using RandomForrestClassifier
############
import subprocess
global playing_flag

def init_music():
    global playing_flag
    playing_flag = 0
    subprocess.call(['osascript', '-e', 'tell application "Spotify" to pause'])

def next():
    global playing_flag
    subprocess.call(['osascript', '-e', 'tell application "Spotify" to play next track'])
    playing_flag = 1

def previous():
    global playing_flag
    subprocess.call(['osascript', '-e', 'tell application "Spotify" to play previous track'])
    playing_flag = 1

def pause_play():
    global playing_flag
    if playing_flag:
        subprocess.call(['osascript', '-e', 'tell application "Spotify" to pause'])
        playing_flag = 0
    else:
        subprocess.call(['osascript', '-e', 'tell application "Spotify" to play'])
        playing_flag = 1