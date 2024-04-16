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
  servo_runner = ServoRunner(baseDir, ifDebug=True)
  light_runner = LightRunner(baseDir, ifDebug=True)

  # light_runner.startFlowByFile("effect1.json")
  durationList = light_runner.getLightJSONDurationByFile('effect1.json')
  servo_runner.moveByFile('servo1.json', durationList)
  # servo_runner;

  # audio_detection_runner.start_regonize()
