#!/usr/bin/env python3
# encoding:utf-8
import sys
sys.path.append('/home/pi/ArmPi/')
import cv2
import time
import numpy as np
import threading
import os

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

class ImageTakerRunner():
    def __init__(self, baseDir, ifDebug=True):
        self.baseDir = baseDir
        self.ifDebug = ifDebug
        self.outputFile = baseDir + "/picture.jpg"
        if ifDebug:
            print(self.outputFile)
    
    def get_picture(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y', 'U', 'Y', 'V'))
        cap.set(cv2.CAP_PROP_FPS, 30)
        cap.set(cv2.CAP_PROP_SATURATION, 40)
        time.sleep(0.2)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(self.outputFile, frame)
        cap.release()
        cv2.destroyAllWindows()
        return
    
    def get_video(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y', 'U', 'Y', 'V'))
        cap.set(cv2.CAP_PROP_FPS, 30)
        cap.set(cv2.CAP_PROP_SATURATION, 40)
        while True:
            ret, frame = cap.read()
            if ret:
                cv2.imshow("frame", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        cap.release()
        cv2.destroyAllWindows()
        return

if __name__ == '__main__':
    cameraRunner = ImageTakerRunner(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
    cameraRunner.get_picture()
    # cameraRunner.get_video()