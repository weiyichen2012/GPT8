#!/usr/bin/env python3
# encoding:utf-8
import sys
sys.path.append('/home/pi/ArmPi/')
import cv2
import time
import numpy as np
import threading
import os
import mediapipe


if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

class Camera:
    def __init__(self, resolution=(640, 480), outputFile='picture.jpg', ifDebug=True):
        self.cap = None
        self.outputFile = outputFile
        self.ifDebug = ifDebug
        self.width = resolution[0]
        self.height = resolution[1]
        self.frame = None
        self.opened = False
        #加载参数
        # self.param_data = np.load(calibration_param_path + '.npz')
        
        #获取参数
        # self.mtx = self.param_data['mtx_array']
        # self.dist = self.param_data['dist_array']
        # self.newcameramtx, roi = cv2.getOptimalNewCameraMatrix(self.mtx, self.dist, (self.width, self.height), 0, (self.width, self.height))
        # self.mapx, self.mapy = cv2.initUndistortRectifyMap(self.mtx, self.dist, None, self.newcameramtx, (self.width,self.height), 5)
        
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
        index = 0;
        while True:
            try:
                if self.opened and self.cap.isOpened():
                    ret, frame_tmp = self.cap.read()

                    if ret:
                        frame_resize = cv2.resize(frame_tmp, (self.width, self.height), interpolation=cv2.INTER_NEAREST)
                        index += 1
                        if index % 100 == 0:
                            if self.ifDebug:
                                print('camera frame')
                            cv2.imwrite(self.outputFile, frame_resize)
                        
                        self.frame = frame_resize

                        # self.frame = cv2.remap(frame_resize, self.mapx, self.mapy, cv2.INTER_LINEAR)
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

class HandRecognitionRunner():
    def __init__(self, baseDir, camera, ifDebug = True):
        self.baseDir = baseDir
        self.camera = camera
        self.selfBaseDir = baseDir + '/handRecognition/'
        self.ifDebug = ifDebug

        self.drawingModule = mediapipe.solutions.drawing_utils
        self.handsModule = mediapipe.solutions.hands
        self.hands = self.handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2)
        self.cnt = [0, 0, 0, 0]

    def get_dist(self, a, b):
        return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2 ) ** 0.5

    def recognize_hand(self):
        img = self.camera.frame
        frame = img

        ifTwoHands = False
        mid_x = 0
        ifGesture_four = False
        ifGesture_lanhua = False
        ifGesture_ok = False

        if frame is not None:
            frame1 = cv2.resize(frame, (640, 480))
            try:
                results = self.hands.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
            except Exception as e:
                print('hand recognition error:', e)
                return ifTwoHands, mid_x, ifGesture_four

            if results.multi_hand_landmarks != None:
                ifTwoHands = len(results.multi_hand_landmarks) == 2
                for handLandmark in results.multi_hand_landmarks:
                    self.drawingModule.draw_landmarks(frame1, handLandmark, self.handsModule.HAND_CONNECTIONS)            
                    pos3 = handLandmark.landmark[3]
                    pos4 = handLandmark.landmark[4]
                    pos8 = handLandmark.landmark[8]
                    pos12 = handLandmark.landmark[12]
                    pos13 = handLandmark.landmark[13]

                    # if self.ifDebug:
                    #     print('twohand:', ifTwoHands)
                    #     print('4:', self.get_dist(pos4, pos13), self.get_dist(pos3, pos4))
                    #     print('lanhua:', self.get_dist(pos4, pos12), self.get_dist(pos3, pos4))
                    #     print('ok:', self.get_dist(pos4, pos8), self.get_dist(pos3, pos4))

                    if self.get_dist(pos4, pos13) < self.get_dist(pos3, pos4):
                        ifGesture_four = True
                    
                    if self.get_dist(pos4, pos12) < self.get_dist(pos3, pos4):
                        ifGesture_lanhua = True
                    
                    if self.get_dist(pos4, pos8) < self.get_dist(pos3, pos4):
                        ifGesture_ok = True

            
            # if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 2:
            #     ifTwoHands = True
            #     mid_x = (results.multi_hand_landmarks[0].landmark[0].x + results.multi_hand_landmarks[1].landmark[0].x) / 2
            #     print(mid_x)



            if self.ifDebug:
                cv2.imshow("Frame", frame1);
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    return

        # if img is not None:
        #     cv2.imshow('img', img)
        #     key = cv2.waitKey(1)
        #     if key == 27:
        #         return
        
        ifTwoHandsOut = False
        ifGesture_fourOut = False
        ifGesture_lanhuaOut = False
        ifGesture_okOut = False

        if ifTwoHands:
            self.cnt[0] += 1
            if self.cnt[0] > 7:
                ifTwoHandsOut = True
        else:
            self.cnt[0] = 0
        

        if ifGesture_four:
            self.cnt[1] += 1
            if self.cnt[1] > 7:
                ifGesture_fourOut = True
        else:
            self.cnt[1] = 0

        if ifGesture_lanhua:
            self.cnt[2] += 1
            if self.cnt[2] > 7:
                ifGesture_lanhuaOut = True
        else:
            self.cnt[2] = 0

        if ifGesture_ok:
            self.cnt[3] += 1
            if self.cnt[3] > 7:
                ifGesture_okOut = True
        else:
            self.cnt[3] = 0

        # print(self.cnt)

        return ifTwoHandsOut, mid_x, ifGesture_fourOut, ifGesture_lanhuaOut, ifGesture_okOut

class ImageTakerRunner():
    def __init__(self, baseDir, ifDebug=True):
        self.baseDir = baseDir
        self.ifDebug = ifDebug
        self.outputFile = baseDir + "/picture.jpg"
        self.my_camera = Camera(resolution=(640, 480), outputFile=self.outputFile, ifDebug=self.ifDebug)
        self.my_camera.camera_open()
        self.handRecognitionRunner = HandRecognitionRunner(baseDir, self.my_camera, ifDebug=self.ifDebug)
        if ifDebug:
            print(self.outputFile)
    
    def recognize_hand(self):
        # while True:
        return self.handRecognitionRunner.recognize_hand()


if __name__ == '__main__':
    imageTakerRunner = ImageTakerRunner(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), ifDebug=True)
    while True:
        print(imageTakerRunner.recognize_hand())
    # my_camera = Camera()
    # my_camera.camera_open()
    # drawingModule = mediapipe.solutions.drawing_utils
    # handsModule = mediapipe.solutions.hands
    # hands = handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2)
    
    # my_camera.camera_close()
    # cv2.destroyAllWindows()