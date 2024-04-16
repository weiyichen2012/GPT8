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

emotionList = ['开心', '悲伤', '中立']
ifTest = True

def getEmotion(ifDebug=True):
  if ifTest:
    sentence = "我很伤心"
  else:
    sentence = audio_detection_runner.get_sentence()
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
  audio_detection_runner = AudioDetectionRunner(baseDir, ifDebug=True)
  emotion_detection_runner = EmotionDetectionRunner(baseDir, ifDebug=True)
  image_taker_runner = ImageTakerRunner(baseDir, ifDebug=False)
  arm_control_runner = ArmControlRunner(baseDir, ifDebug=True)
  servo_runner = ServoRunner(baseDir, ifDebug=True)
  light_runner = LightRunner(baseDir, ifDebug=True)

  audio_detection_runner.start_regonize()
  # possibility_text = emotion_detection_runner.get_emotion_text("我很伤心")

  while True:
    print("wait for microphone, 20 seconds")
    time.sleep(20.0)
    emotion = getEmotion()
    print("get emotion: ", emotion)
    if emotion == '悲伤':
      print('detect sad')
      light_runner.startFlowByFile("effect1.json")
      # arm_control_runner.moveArmByFile('1 fast forward.d6a')
      
      print("recognize hand")
      
      ifRecognizeFour = False
      for i in range(0, 60):
        ifTwoHandsOut, mid_x, ifGesture_fourOut, ifGesture_lanhuaOut, ifGesture_okOut = image_taker_runner.recognize_hand()
        if ifGesture_fourOut:
          ifRecognizeFour = True
          break
    
      if ifRecognizeFour:
        print("recognize four")
        servo_runner.move(0)
        servo_runner.moveByListAsync([90, 0, 90, 0, 90, 0, 90, 0, 90, 0], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
        print("wait for microphone, 20 seconds")
        time.sleep(20.0)
        setence = audio_detection_runner.get_sentence()
        print("get sentence: ", setence)

        ifRecognizeTwoHands = False
        for i in range(0, 60):
          ifTwoHandsOut, mid_x, ifGesture_fourOut, ifGesture_lanhuaOut, ifGesture_okOut = image_taker_runner.recognize_hand()
          if ifTwoHandsOut:
            ifRecognizeTwoHands = True
            break
        
        if ifRecognizeTwoHands:
          print("recognize two hands, reset ")
          continue

        if "焦虑" in setence or "压力":
          print("焦虑压力")
          light_runner.startFlowByFile("effect1.json")
          durationList = light_runner.getLightJSONDurationByFile('effect1.json')
          servo_runner.moveByFile('servo1.json', durationList)
          
          durationSum = 0.0
          for duration in durationList:
            durationSum += duration
          time.sleep(durationSum)
          # arm_control_runner.moveArmByFile('1 fast forward.d6a')
        else:
          ...
        # arm_control_runner.moveArmByFile('1 fast forward.d6a')
      else:
        print("not recognize four")
        light_runner.startFlowByFile("effect2.json")
        continue

  # durationList = light_runner.getLightJSONDurationByFile('effect1.json')
  # light_runner.startFlowByFile("effect1.json")
  # arm_control_runner.moveArmByFile('arm1.json', durationList)
  # servo_runner;

