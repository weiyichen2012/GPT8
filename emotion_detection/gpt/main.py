import base64
import requests

def get_emotion_text(text: str) -> str:
  f = open("api_key", "r")
  api_key = f.readline()

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
            "text": "一个人说" + text + "他的情绪是以下哪种？开心，悲伤，愤怒，焦虑，无聊，恐惧，惊讶，厌恶，烦躁，中立。无需其他内容，仅仅回答每种情绪的可能性，用数字%表达。"
          }
        ]
      }
    ],
    "max_tokens": 300
  }

  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, proxies={"https": "http://127.0.0.1:1080"})
  print(response.json()["choices"][0]['message']['content'])
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
  # get_emotion_text("学习好累我不想干了。")
  get_emotion_image("hqx_happy.jpg")
