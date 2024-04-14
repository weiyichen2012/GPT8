import os
from audio_detection.main import AudioDetectionRunner
from emotion_detection.gpt.emotion_detection import EmotionDetectionRunner
from image_taker.image import ImageTakerRunner
from armControl.armControl import ArmControlRunner
# from handRecognition.hand import HandRecognitionRunner
import time

emotionList = ['开心', '悲伤', '中立']

# def testHandRecognition(image_taker_runner):
#   while True:
#     image_taker_runner.recognize_hand()

def handFollow(ifDebug=True):
  ifTwoHands, mid_x, ifGesture1 = image_taker_runner.recognize_hand()
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

  time.sleep(10)
  emotion = getEmotion()
  print(emotion)
  # if emotion == '悲伤':
  #   handFollow()
  # handFollow()

# print(baseDir)
