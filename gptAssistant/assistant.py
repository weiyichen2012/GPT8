from openai import OpenAI
import time
import os
import json

os.environ['http_proxy'] = 'localhost:1080'
os.environ['https_proxy'] = 'localhost:1080'

class AssistantRunner():
  def __init__(self, baseDir, assistant_id="asst_Yqgv3u1O7SoJ0k4Bu2shxz6y", thread_id="thread_uvIpVGfP3HxnCGr4AgaBT9KU") -> None:
    os.chdir(baseDir)
    print(baseDir)
    f = open("api_key", "r")
    api_key = f.readline()
    self.api_key = api_key

    self.baseDir = baseDir + "/gptAssistant"
    self.assistant_id = assistant_id
    self.thread_id = thread_id
    self.client = OpenAI(api_key=api_key)
    return

  def ask(self, msg):
    message = self.client.beta.threads.messages.create(
    thread_id=self.thread_id,
    role="user",
    content=msg
    )

    run = self.client.beta.threads.runs.create(
      thread_id=self.thread_id,
      assistant_id=self.assistant_id,
      # instructions="Please address the user as Jane Doe. The user has a premium account."
    )

    while run.status != 'completed':
      run = self.client.beta.threads.runs.retrieve(thread_id=self.thread_id, run_id=run.id)
      print(run.status)
      time.sleep(.3)

    if run.status == 'completed': 
      messages = self.client.beta.threads.messages.list(
        thread_id=self.thread_id
      )
      print(messages.data[0].content[0].text.value)
      return messages.data[0].content[0].text.value
    else:
      print("error")
      return ""

if __name__ == "__main__":
  assistantRunner = AssistantRunner(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
  assistantRunner.ask("What's the answer of 1+1")