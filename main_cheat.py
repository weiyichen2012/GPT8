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

cheatTwoHands = True #False 代表作弊，true代表识别

emotionList = ['开心', '悲伤', '中立']

# def getEmotion(ifDebug=True):
#   sentence = "我很伤心"
#   possibility_text = emotion_detection_runner.get_emotion_text(sentence)
#   possibility_image = emotion_detection_runner.get_emotion_image("picture.jpg")
#
#   maxEmotion = emotionList[0]
#   maxPossibility = possibility_image[0] + possibility_text[0]
#
#   for i in range(1, len(emotionList)):
#     if possibility_image[i] + possibility_text[i] > maxPossibility:
#       maxEmotion = emotionList[i]
#       maxPossibility = possibility_image[i] + possibility_text[i]
#
#   if ifDebug:
#     print("Audio: ", sentence)
#     print("detection finished\n", possibility_text, possibility_image)
#     print("Emotion: ", maxEmotion, maxPossibility)
#
#   return maxEmotion

if __name__ == '__main__':
  baseDir = '/home/pi/GPT8/'
  audio_detection_runner = AudioDetectionRunner(baseDir, ifDebug=False)
  emotion_detection_runner = EmotionDetectionRunner(baseDir, ifDebug=False)
  image_taker_runner = ImageTakerRunner(baseDir, ifDebug=True)
  arm_control_runner = ArmControlRunner(baseDir, ifDebug=False)
  servo_runner = ServoRunner(baseDir, ifDebug=False)
  light_runner = LightRunner(baseDir, ifDebug=False)

  audio_detection_runner.start_regonize()
  # possibility_text = emotion_detection_runner.get_emotion_text("我很伤心")

  # arm_control_runner.moveArmFile('1 fast forward.d6a')

#除了必要的动的部分其他全靠我们演
  while True:
    print("wait for microphone, 20 seconds")
    time.sleep(20.0)
    print('detect sad')
    light_runner.startFlowByFile("wave.json")
    arm_control_runner.moveArmFile('1 fast forward.d6a')      
    print("recognize hand")
    time.sleep(10.0)  #等我们做出手势

    # 识别到光球汇聚后的语音识别，触发后续对应程序
    print("recognize four")
    servo_runner.move(0)
    servo_runner.moveByListAsync([90, 0, 90, 0, 90, 0, 90, 0, 90, 0], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
    print("wait for microphone for 焦虑压力, 20 seconds")
    time.sleep(20.0)
    print("prepare to detect two hands")
    time.sleep(10.0)
    print("detect 焦虑压力")
    light_runner.startFlowByFile("wave.json")
    durationList = light_runner.getLightJSONDurationByFile('wave.json')
    servo_runner.moveByFile('servo1.json', durationList)
    arm_control_runner.moveArmFileList(['1 fast backward.d6a', '1 fast forward.d6a', '1 fast backward.d6a', '1 fast forward.d6a'])
    

    durationSum = 0.0
    for duration in durationList:
      durationSum += duration
    time.sleep(durationSum)
