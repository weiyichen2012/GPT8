import base64
import requests
import time
import regex

emotionList = ['开心', '悲伤', '中立']

def get_emotion_text(text: str) -> str:
  f = open("api_key", "r")
  api_key = f.readline()

  sentence = ""
  for i in range(0, len(emotionList)):
    if i == len(emotionList) - 1:
      sentence += emotionList[i] + "."
    else:
      sentence += emotionList[i] + ", "
  sentence = "如果你听到有人说\"" + text + "\", 他是哪种情绪?" + sentence
  sentence += " 用数字与%表达没种情绪的可能性，总和应为100%。只需回答情绪+数字。"
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
  print(content)
  for i in range(0, len(emotionList)):
    possibility = regex.regex.findall(emotionList[i] + r".*?([\d]+)%", content)
    if possibility:
      possibility = possibility[0]
    else:
      possibility = 0.0
    print(emotionList[i], possibility)
  return response

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def get_emotion_image(image_path: str) -> str:
  f = open("api_key", "r")
  api_key = f.readline()

  base64_image = encode_image(image_path)

  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
  }

  payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "图中人的情绪是以下哪种？开心，悲伤，愤怒，焦虑，无聊，恐惧，惊讶，厌恶，烦躁。仅仅回答每种情绪的可能性，用数字%表达。"
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
  print(response.json()["choices"][0]['message']['content'])
  return response

if __name__ == "__main__":
  t1 = time.time()
  # get_emotion_text("I'm so tired of studying")
  get_emotion_text("这游戏太好玩了")
  # get_emotion_image("hqx_happy.jpg")
  t2 = time.time()
  print("Used time: ", t2 - t1, "s")