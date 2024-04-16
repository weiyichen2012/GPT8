import base64
import requests
import time
import regex
import os

emotionList = ['开心', '悲伤', '中立']

class EmotionDetectionRunner():
  def __init__(self, baseDir, ifDebug=True) -> None:
    self.baseDir = baseDir
    self.selfBaseDir = baseDir + "/emotion_detection/gpt"
    self.ifDebug = ifDebug
    return
  
  def get_emotion_text(self, text: str) -> str:
    # os.chdir(self.baseDir)
    print(self.baseDir)
    f = open(self.baseDir + "api_key", "r")
    api_key = f.readline()
    api_key = api_key.strip("\n")

    sentence = ""
    for i in range(0, len(emotionList)):
      if i == len(emotionList) - 1:
        sentence += emotionList[i] + "."
      else:
        sentence += emotionList[i] + ", "
    sentence = "如果你听到有人说\"" + text + "\", 他是哪种情绪?" + sentence
    sentence += " 用数字与%表达没种情绪的可能性，总和应为100%。只需回答情绪+数字。"

    if self.ifDebug:
      print(sentence)

    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
    }

    payload = {
      "model": "gpt-4-turbo-preview",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": sentence
            }
          ]
        }
      ],
      "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, proxies={"https": "http://127.0.0.1:1080"})
    content = response.json()["choices"][0]['message']['content']
    if self.ifDebug:
      print(content)
    
    possibilityList = []
    for i in range(0, len(emotionList)):
      possibility = regex.regex.findall(emotionList[i] + r".*?([\d]+)%", content)
      if possibility:
        possibility = possibility[0]
      else:
        possibility = 0.0
      possibilityList.append(float(possibility))
      if self.ifDebug:
        print(emotionList[i], possibility)
    return possibilityList

  def encode_image(self, image_path):
    with open(image_path, "rb") as image_file:
      return base64.b64encode(image_file.read()).decode('utf-8')

  def get_emotion_description(self, image_path):
    # os.chdir(self.baseDir)
    f = open(self.baseDir + "api_key", "r")
    api_key = f.readline()
    api_key = api_key.strip("\n")

    base64_image = self.encode_image(self.baseDir + image_path)

    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
    }

    # sentence = "你现在是一名专业的心理学家和微表情学家，请你详细分析图中情绪。"
    sentence = "做情感情绪。"
    if self.ifDebug:
      print(sentence)

    payload = {
      "model": "gpt-4-vision-preview",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": sentence
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              }
            }
          ]
        }
      ],
      "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, proxies={"https": "http://127.0.0.1:1080"})
    content = response.json()["choices"][0]['message']['content']
    return content


  def get_emotion_image(self, image_path: str) -> str:
    # os.chdir(self.baseDir)
    f = open(self.baseDir + "api_key", "r")
    api_key = f.readline()
    api_key = api_key.strip("\n")

    base64_image = self.encode_image(self.baseDir + image_path)

    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
    }

    sentence = ""
    for i in range(0, len(emotionList)):
      if i == len(emotionList) - 1:
        sentence += emotionList[i] + "."
      else:
        sentence += emotionList[i] + ", "
    # sentence = "分析情绪是以下哪种？" + sentence
    sentence += " 用数字与%表达每种情绪的可能性，总和应为100%。只需回答情绪+数字。"
    if self.ifDebug:
      print(sentence)

    payload = {
      "model": "gpt-4-vision-preview",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": sentence
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              }
            }
          ]
        }
      ],
      "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, proxies={"https": "http://127.0.0.1:1080"})
    content = response.json()["choices"][0]['message']['content']
    if self.ifDebug:
      print(content)

    possibilityList = []
    for i in range(0, len(emotionList)):
      possibility = regex.regex.findall(emotionList[i] + r".*?([\d]+)%", content)
      if possibility:
        possibility = possibility[0]
      else:
        possibility = 0.0
      possibilityList.append(float(possibility))
      if self.ifDebug:
        print(emotionList[i], possibility)
    return possibilityList

if __name__ == "__main__":
  emotionDetectionRunner = EmotionDetectionRunner("../../")
  t1 = time.time()
  # emotionDetectionRunner.get_emotion_text("I'm so tired of studying")
  emotionDetectionRunner.get_emotion_text("我很伤心")
  # emotionDetectionRunner.get_emotion_image("hqx_happy.jpg")
  t2 = time.time()
  print("Used time: ", t2 - t1, "s")