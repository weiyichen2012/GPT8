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

# 以下两个cheat为两个开关，通过布尔值真假控制程序的自主程度
cheatEmotionDetection = False  # True 代表在最开始的情绪识别就作弊，无论什么情绪都识别为悲伤
cheatTwoHands = False  # False 代表在手势识别阶段作弊，无论什么手势都执行语音触发的四种效果
cheatInputWords = True

emotionList = ['开心', '悲伤', '中立']
ifTest = False


def getEmotion(ifDebug=True):
    # sentence = audio_detection_runner.get_sentence()

    # possibility_text = emotion_detection_runner.get_emotion_text("sentence")
    possibility_image = emotion_detection_runner.get_emotion_image("picture.jpg")

    maxEmotion = emotionList[0]
    # maxPossibility = possibility_image[0] + possibility_text[0]

    for i in range(1, len(emotionList)):
        if possibility_image[i] > maxPossibility:
            maxEmotion = emotionList[i]
            maxPossibility = possibility_image[i]

    if ifDebug:
        # print("detection finished\n", possibility_text, possibility_image)
        print("Emotion: ", maxEmotion, maxPossibility)

    return maxEmotion


if __name__ == '__main__':
    baseDir = '/home/pi/GPT8/'
    audio_detection_runner = AudioDetectionRunner(baseDir, ifDebug=False)
    emotion_detection_runner = EmotionDetectionRunner(baseDir, ifDebug=False)
    image_taker_runner = ImageTakerRunner(baseDir, ifDebug=True)  # 设成True打开窗口
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
        if emotion == '悲伤' or cheatEmotionDetection:
            randN = random.randint(0, 12)
            print(randN)
            if randN == 0:
                ...
            elif randN == 1:
                ...

