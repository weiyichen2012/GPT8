import os
from audio_detection.main import AudioDetectionRunner
from emotion_detection.gpt.emotion_detection import EmotionDetectionRunner
from image_taker.image import ImageTakerRunner
from armControl.armControl import ArmControlRunner
from light.light import LightRunner
# from handRecognition.hand import HandRecognitionRunner
import time
from yeelight import *

emotionList = ['开心', '悲伤', '中立']

# def testHandRecognition(image_taker_runner):
#   while True:
#     image_taker_runner.recognize_hand()

def handFollow(ifDebug=True):
  ifTwoHands, mid_x, ifGesture_four, ifGesture_lanhua, ifGesture_ok = image_taker_runner.recognize_hand()
  if ifTwoHands:
    currPos = arm_control_runner.getArmPos()
    if mid_x < 0.4:
      currPos[5] -= 1
    elif mid_x > 0.6:
      currPos[5] += 1
    arm_control_runner.moveArm(50, currPos)
    print(mid_x, "Move to: ", currPos[5])
  time.sleep(0.06)

def getEmotion(ifDebug=True):
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
  baseDir = os.path.dirname(os.path.abspath(__file__))
  audio_detection_runner = AudioDetectionRunner(baseDir, ifDebug=True)
  emotion_detection_runner = EmotionDetectionRunner(baseDir, ifDebug=True)
  image_taker_runner = ImageTakerRunner(baseDir, ifDebug=True)
  arm_control_runner = ArmControlRunner(baseDir, ifDebug=True)
  audio_detection_runner.start_regonize()

  time.sleep(13)
  emotion = getEmotion()
  description  = emotion_detection_runner.get_emotion_description("picture.jpg")
  print(description)

  lightRunner = LightRunner(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
  transitions = [
      RGBTransition(0, 0, 128, duration=3000, brightness=10),  # 深蓝色，低亮度，模拟天空刚开始亮起
      RGBTransition(255, 140, 0, duration=3000, brightness=60),  # 橙红色，中等亮度，模拟太阳刚刚升起
      RGBTransition(255, 215, 0, duration=3000, brightness=100),  # 金黄色，高亮度，模拟太阳完全升起
  ]
  if emotion == '悲伤':
    lightRunner.startFlow(transitions)

  # print(description)
  # if emotion == '悲伤':
  #   handFollow()
  # handFollow()

# print(baseDir)
