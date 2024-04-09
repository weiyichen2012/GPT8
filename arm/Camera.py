#!/usr/bin/env python3
# encoding:utf-8
import sys
sys.path.append('/home/pi/ArmPi/')
import cv2
import time
import threading
import numpy as np
from CameraCalibration.CalibrationConfig import *

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

class Camera:
    def __init__(self, resolution=(640, 480)):
        self.cap = None
        self.width = resolution[0]
        self.height = resolution[1]
        self.frame = None
        self.opened = False
        #加载参数
        self.param_data = np.load(calibration_param_path + '.npz')
        
        #获取参数
        self.mtx = self.param_data['mtx_array']
        self.dist = self.param_data['dist_array']
        self.newcameramtx, roi = cv2.getOptimalNewCameraMatrix(self.mtx, self.dist, (self.width, self.height), 0, (self.width, self.height))
        self.mapx, self.mapy = cv2.initUndistortRectifyMap(self.mtx, self.dist, None, self.newcameramtx, (self.width,self.height), 5)
        
        self.th = threading.Thread(target=self.camera_task, args=(), daemon=True)
        self.th.start()

    def camera_open(self):
        try:
            self.cap = cv2.VideoCapture(-1)
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y', 'U', 'Y', 'V'))
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            self.cap.set(cv2.CAP_PROP_SATURATION, 40)
            self.opened = True
        except Exception as e:
            print('打开摄像头失败:', e)

    def camera_close(self):
        try:
            self.opened = False
            time.sleep(0.2)
            if self.cap is not None:
                self.cap.release()
                time.sleep(0.05)
            self.cap = None
        except Exception as e:
            print('关闭摄像头失败:', e)

    def camera_task(self):
        while True:
            try:
                if self.opened and self.cap.isOpened():
                    ret, frame_tmp = self.cap.read()
                    if ret:
                        frame_resize = cv2.resize(frame_tmp, (self.width, self.height), interpolation=cv2.INTER_NEAREST)
                        self.frame = cv2.remap(frame_resize, self.mapx, self.mapy, cv2.INTER_LINEAR)
                    else:
                        print(1)
                        self.frame = None
                        cap = cv2.VideoCapture(-1)
                        ret, _ = cap.read()
                        if ret:
                            self.cap = cap
                elif self.opened:
                    print(2)
                    cap = cv2.VideoCapture(-1)
                    ret, _ = cap.read()
                    if ret:
                        self.cap = cap              
                else:
                    time.sleep(0.01)
            except Exception as e:
                print('获取摄像头画面出错:', e)
                time.sleep(0.01)

#Import the necessary Packages for this software to run
import mediapipe

if __name__ == '__main__':
    my_camera = Camera()
    my_camera.camera_open()
    drawingModule = mediapipe.solutions.drawing_utils
    handsModule = mediapipe.solutions.hands
    hands = handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2)
    
    while True:
        img = my_camera.frame
        
        #Use CV2 Functionality to create a Video stream and add some values
        # cap = cv2.VideoCapture(0)
        # fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

        #Add confidence values and extra settings to MediaPipe hand tracking. As we are using a live video stream this is not a static
        #image mode, confidence values in regards to overall detection and tracking and we will only let two hands be tracked at the same time
        #More hands can be tracked at the same time if desired but will slow down the system

        #Create an infinite loop which will produce the live feed to our desktop and that will search for hands
        frame = img
        #Unedit the below line if your live feed is produced upsidedown
        #flipped = cv2.flip(frame, flipCode = -1)
        
        #Determines the frame size, 640 x 480 offers a nice balance between speed and accurate identification
        if frame is not None:
            frame1 = cv2.resize(frame, (640, 480))
            
            #Produces the hand framework overlay ontop of the hand, you can choose the colour here too)
            results = hands.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
            
            #In case the system sees multiple hands this if statment deals with that and produces another hand overlay
            if results.multi_hand_landmarks != None:
                for handLandmarks in results.multi_hand_landmarks:
                    drawingModule.draw_landmarks(frame1, handLandmarks, handsModule.HAND_CONNECTIONS)
                    
                    #Below is Added Code to find and print to the shell the Location X-Y coordinates of Index Finger, Uncomment if desired
                    #for point in handsModule.HandLandmark:
                        
                        #normalizedLandmark = handLandmarks.landmark[point]
                        #pixelCoordinatesLandmark= drawingModule._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, 640, 480)
                        
                        #Using the Finger Joint Identification Image we know that point 8 represents the tip of the Index Finger
                        #if point == 8:
                            #print(point)
                            #print(pixelCoordinatesLandmark)
                            #print(normalizedLandmark)
                
            #Below shows the current frame to the desktop 
            cv2.imshow("Frame", frame1);
            key = cv2.waitKey(1) & 0xFF
            
            #Below states that if the |q| is press on the keyboard it will stop the system
            if key == ord("q"):
                break

        if img is not None:
            cv2.imshow('img', img)
            key = cv2.waitKey(1)
            if key == 27:
                break
    my_camera.camera_close()
    cv2.destroyAllWindows()