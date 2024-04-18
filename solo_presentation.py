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

cheatEmotionDetection = True  # True 代表作弊，自动悲伤
cheatTwoHands = False  # False 代表作弊，不识别

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
    image_taker_runner = ImageTakerRunner(baseDir, ifDebug=True)  # 设成True打开拍照窗口
    arm_control_runner = ArmControlRunner(baseDir, ifDebug=False)
    servo_runner = ServoRunner(baseDir, ifDebug=False)
    light_runner = LightRunner(baseDir, ifDebug=False)

   #通过注释和解注释,用input去隔开（input不一定正确，需要多个）
    #先复位
    # arm_control_runner.moveArmFile('reset.d6a')

    # #这就是lighbo
    # input()
    # light_runner.startFlowByFile('wave.json')
    # durationList = light_runner.getLightJSONDurationByFile('wave.json')
    # servo_runner.moveByFile('servo_waves.json', durationList)
    # arm_control_runner.moveArmFile('17 waves.d6a')

    #演示暗示
    # input()
    light_runner.startFlowByFile('hint.json')
    arm_control_runner.moveArmFile('21 hint.d6a')

    #演示光球汇聚
    input()
    arm_control_runner.moveArmFile('22 see you.d6a')
    servo_runner.move(0)
    #演示对话时会变焦
    input()
    servo_runner.moveByListAsync([180, 0, 180, 0, 180, 0], [2, 2, 2, 2, 2, 2])

    #演示日出的自我表达
    input()
    light_runner.startFlowByFile("sunrise.json")
    durationList = light_runner.getLightJSONDurationByFile('sunrise.json')
    servo_runner.moveByFile('servo_sunrise.json', durationList)
    arm_control_runner.moveArmFile('20 sun rise.d6a')

    #创新点论证：模仿自然节律
    input()
    light_runner.startFlowByFile('firefly.json')
    #创新点论证：抽象段落
    light_runner.startFlowByFile('color.json')
    #创新点论证：机械臂的基础动作库
    input()
    arm_control_runner.moveArmFileList(['1 slowly forward.d6a', '2 slowly backward.d6a', '3 turn left fast.d6a', '4 turn right slowly.d6a', '5 tilt the head left fast.d6a', 'n head up slowly.d6a'])