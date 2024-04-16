import os
from audio_detection.main import AudioDetectionRunner
from emotion_detection.gpt.emotion_detection import EmotionDetectionRunner
from image_taker.image import ImageTakerRunner
from armControl.armControl import ArmControlRunner
from light.light import LightRunner
from servo.servo import ServoRunner
# from handRecognition.hand import HandRecognitionRunner
import time
from yeelight import *
import random

cheatEmotionDetection = True #True 代表作弊，自动悲伤
cheatTwoHands = False #False 代表作弊，不识别

emotionList = ['开心', '悲伤', '中立']
ifTest = False

def getEmotion(ifDebug=True):
  sentence = "我很伤心"
  possibility_text = emotion_detection_runner.get_emotion_text(sentence)
  possibility_image = emotion_detection_runner.get_emotion_image("picture.jpg")

  maxEmotion = emotionList[0]
  maxPossibility = possibility_image[0] + possibility_text[0]

  for i in range(1, len(emotionList)):
    if possibility_image[i] + possibility_text[i] > maxPossibility:
      maxEmotion = emotionList[i]
      maxPossibility = possibility_image[i] + possibility_text[i]
  
  if ifDebug:
    print("Audio: ", sentence)
    print("detection finished\n", possibility_text, possibility_image)
    print("Emotion: ", maxEmotion, maxPossibility)
  
  return maxEmotion

if __name__ == '__main__':
  baseDir = '/home/pi/GPT8/'
  audio_detection_runner = AudioDetectionRunner(baseDir, ifDebug=False)
  emotion_detection_runner = EmotionDetectionRunner(baseDir, ifDebug=False)
  image_taker_runner = ImageTakerRunner(baseDir, ifDebug=True)#设成True打开窗口
  arm_control_runner = ArmControlRunner(baseDir, ifDebug=False)
  servo_runner = ServoRunner(baseDir, ifDebug=False)
  light_runner = LightRunner(baseDir, ifDebug=False)

  audio_detection_runner.start_regonize()
  # possibility_text = emotion_detection_runner.get_emotion_text("我很伤心")

  # arm_control_runner.moveArmFile('1 fast forward.d6a')


  while True:
    print("wait for microphone, 20 seconds")
    time.sleep(20.0)
    emotion = getEmotion()
    print("get emotion: ", emotion)
    if emotion == '悲伤' or cheatTwoHands:
      print('detect sad')
      light_runner.startFlowByFile("effect1.json")
      arm_control_runner.moveArmFile('1 fast forward.d6a')
      
      print("recognize hand")
      
      ifRecognizeFour = True
      for i in range(0, 300):
        ifTwoHandsOut, mid_x, ifGesture_fourOut, ifGesture_lanhuaOut, ifGesture_okOut = image_taker_runner.recognize_hand()
        if ifGesture_fourOut:
          ifRecognizeFour = True
          break

      # 识别到光球汇聚后的语音识别，触发后续对应程序
      if ifRecognizeFour:
        print("recognize four")
        servo_runner.move(0)
        servo_runner.moveByListAsync([90, 0, 90, 0, 90, 0, 90, 0, 90, 0], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
        print("wait for microphone for 焦虑压力, 20 seconds")
        time.sleep(20.0)
        sentence = audio_detection_runner.get_sentence()
        print("get sentence: ", sentence)

        ifRecognizeTwoHands = False
        for i in range(0, 300):
          ifTwoHandsOut, mid_x, ifGesture_fourOut, ifGesture_lanhuaOut, ifGesture_okOut = image_taker_runner.recognize_hand()
          if ifTwoHandsOut:
            ifRecognizeTwoHands = True
            break
        
        if ifRecognizeTwoHands and cheatTwoHands:
          print("recognize two hands, reset ")
          continue

        if "考试" in sentence or "焦虑" in sentence or "压力" in sentence:
        # print("焦虑压力")
          light_runner.startFlowByFile("effect1.json")
          durationList = light_runner.getLightJSONDurationByFile('effect1.json')
          servo_runner.moveByFile('servo1.json', durationList)
          arm_control_runner.moveArmFileList(['1 fast forward.d6a', '1 fast forward.d6a', '1 fast forward.d6a'])

          durationSum = 0.0
          for duration in durationList:
            durationSum += duration
          time.sleep(durationSum)
        #仿照这里写
        elif "实习" in sentence or "上学" in sentence or "通宵" in sentence:
          light_runner.startFlowByFile("effect1.json")
          durationList = light_runner.getLightJSONDurationByFile('effect1.json')
          servo_runner.moveByFile('servo1.json', durationList)
          arm_control_runner.moveArmFileList(['1 fast forward.d6a', '1 fast forward.d6a', '1 fast forward.d6a'])

          durationSum = 0.0
          for duration in durationList:
            durationSum += duration
          time.sleep(durationSum)
        else:
          #随机执行
          if random.random() < 0.5:
            light_runner.startFlowByFile("effect1.json")
            durationList = light_runner.getLightJSONDurationByFile('effect1.json')
            servo_runner.moveByFile('servo1.json', durationList)
            arm_control_runner.moveArmFileList(['1 fast forward.d6a', '1 fast forward.d6a', '1 fast forward.d6a'])

            durationSum = 0.0
            for duration in durationList:
              durationSum += duration
            time.sleep(durationSum)
          else:
            light_runner.startFlowByFile("effect2.json")
            durationList = light_runner.getLightJSONDurationByFile('effect2.json')
            servo_runner.moveByFile('servo1.json', durationList)
            arm_control_runner.moveArmFileList(['1 slow forward.d6a', '1 slow forward.d6a', '1 slow forward.d6a'])

            durationSum = 0.0
            for duration in durationList:
              durationSum += duration
            time.sleep(durationSum)

        # else:
        #   ...
        # arm_control_runner.moveArmFile('1 fast forward.d6a')
      else:
        print("not recognize four")
        light_runner.startFlowByFile("effect2.json")
        continue

  # durationList = light_runner.getLightJSONDurationByFile('effect1.json')
  # light_runner.startFlowByFile("effect1.json")
  # arm_control_runner.moveArmFile('arm1.json', durationList)
  # servo_runner;

