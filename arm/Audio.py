import speech_recognition as sr

# 创建Recognizer对象
r = sr.Recognizer()

# 使用麦克风录音
with sr.Microphone() as source:
    print("请说话...")
    audio = r.listen(source)

try:
    # 识别语音
    text = r.recognize_google(audio, language='zh-CN')
    print("你说的是：" + text)
except sr.UnknownValueError:
    print("无法识别语音")
except sr.RequestError as e:
    print("请求出错：{0}".format(e))