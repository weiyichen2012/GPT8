#!/usr/bin/env python3
# encoding:utf-8
import sys
sys.path.append('/home/pi/ArmPi/')
import cv2
import time
import numpy as np
import threading

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

class EmotionCameraRunner():
    def __init__(self, baseDir):
        self.baseDir = baseDir
        self.outputFile = baseDir + "/emotion_detection/gpt/picture.jpg"
    
    def get_picture(self):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(self.outputFile, frame)
        cap.release()
        cv2.destroyAllWindows()
        return

if __name__ == '__main__':
    emotionCameraRunner = EmotionCameraRunner("/home/pi/GPT8")
    emotionCameraRunner.get_picture()