import os
from audio_detection.main import AudioDetectionRunner
from emotion_detection.gpt.main import EmotionDetectionRunner
from image_taker.image import EmotionCameraRunner
from armControl.armControl import ArmControlRunner
import time

emotionList = ['开心', '悲伤', '中立']

if __name__ == '__main__':
  baseDir = os.path.dirname(os.path.abspath(__file__))
  audio_detection_runner = AudioDetectionRunner(baseDir)
  emotion_detection_runner = EmotionDetectionRunner(baseDir)
  image_taker_runner = EmotionCameraRunner(baseDir)
  arm_control_runner = ArmControlRunner(baseDir)

  actionList = arm_control_runner.readArmFile("action1.d6a")
  arm_control_runner.moveArmActionList(actionList)
  arm_control_runner.waitActionFinish()

  # audio_detection_runner.start_regonize()
  # time.sleep(10)
  # sentence = audio_detection_runner.get_sentence()
  # print("Audio: ", sentence)
  # possibility_text = emotion_detection_runner.get_emotion_text(sentence)
  # image_taker_runner.get_picture()
  # possibility_image = emotion_detection_runner.get_emotion_image("picture.jpg")

  # for i in range(0, len(emotionList)):
    # print(emotionList[i], possibility_text[i], possibility_image[i])

# print(baseDir)