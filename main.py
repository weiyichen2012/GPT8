import os
import audio_detection.main as audio_detection
import emotion_detection.gpt.main as prediction_train
import image_taker.image as image_taker
import time

emotionList = ['开心', '悲伤', '中立']

if __name__ == '__main__':
  baseDir = os.path.dirname(os.path.abspath(__file__))
  audio_detection_runner = audio_detection.AudioDetectionRunner(baseDir)
  emotion_detection_runner = prediction_train.EmotionDetectionRunner(baseDir)
  image_taker_runner = image_taker.EmotionCameraRunner(baseDir)

  audio_detection_runner.start_regonize()
  time.sleep(10)
  sentence = audio_detection_runner.get_sentence()
  print("Audio: ", sentence)
  possibility_text = emotion_detection_runner.get_emotion_text(sentence)
  image_taker_runner.get_picture()
  possibility_image = emotion_detection_runner.get_emotion_image("picture.jpg")

  for i in range(0, len(emotionList)):
    print(emotionList[i], possibility_text[i], possibility_image[i])

# print(baseDir)