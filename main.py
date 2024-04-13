import os
from audio_detection.main import AudioDetectionRunner
from emotion_detection.gpt.emotion_detection import EmotionDetectionRunner
from image_taker.image import ImageTakerRunner
from armControl.armControl import ArmControlRunner
from handRecognition.hand import HandRecognitionRunner
import time

emotionList = ['开心', '悲伤', '中立']

def testHandRecognition(image_taker_runner, hand_recognition_runner):
  while True:
    image_taker_runner.get_picture()
    time.sleep(1.0)
    hand_recognition_runner.recognize_hand('picture.jpg')

if __name__ == '__main__':
  baseDir = os.path.dirname(os.path.abspath(__file__))

  audio_detection_runner = AudioDetectionRunner(baseDir, ifDebug=True)
  emotion_detection_runner = EmotionDetectionRunner(baseDir, ifDebug=True)
  image_taker_runner = ImageTakerRunner(baseDir, ifDebug=True)
  arm_control_runner = ArmControlRunner(baseDir, ifDebug=True)
  hand_recognition_runner = HandRecognitionRunner(baseDir, ifDebug=True)

  testHandRecognition(image_taker_runner, hand_recognition_runner)

  # actionList = arm_control_runner.readArmFile("reset.d6a")
  # # arm_control_runner.moveArmActionList(actionList)
  # # arm_control_runner.moveArm(1000, [500, 500, 388, 871, 150, 500])
  # # arm_control_runner.moveArmActionList(actionList)
  # # arm_control_runner.waitActionFinish()

  # audio_detection_runner.start_regonize()
  # time.sleep(10)
  # image_taker_runner.get_picture()
  # sentence = audio_detection_runner.get_sentence()
  # print("Audio: ", sentence)
  # possibility_text = emotion_detection_runner.get_emotion_text(sentence)
  # possibility_image = emotion_detection_runner.get_emotion_image("picture.jpg")

  # print("detection finished\n", possibility_text, possibility_image)
  # for i in range(0, len(emotionList)):
  #   print(emotionList[i], possibility_text[i], possibility_image[i])

# print(baseDir)
