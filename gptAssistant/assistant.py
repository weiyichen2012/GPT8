from openai import OpenAI
import time
import os
import json
import regex

# os.environ['http_proxy'] = 'localhost:1080'
os.environ['https_proxy'] = 'localhost:1080'

class AssistantRunner():
  def __init__(self, baseDir, assistant_id="asst_ut9FZHED4E6pS5MaKAgDsqio", thread_id="thread_iyopchhwZbtjmCjcI4BIeuCB") -> None:
    # os.chdir(baseDir)
    print(baseDir)
    f = open(self.baseDir + "api_key", "r")
    api_key = f.readline()
    self.api_key = api_key

    self.baseDir = baseDir + "/gptAssistant"
    self.assistant_id = assistant_id
    self.thread_id = thread_id
    self.client = OpenAI(api_key=api_key)
    return

  def ask(self, msg):
    # os.environ['http_proxy'] = 'localhost:1080'
    # os.environ['https_proxy'] = 'localhost:1080'
    # time.sleep(1)

    # print("env", os.environ['http_proxy'], os.environ['https_proxy'])

    message = self.client.beta.threads.messages.create(
      thread_id=self.thread_id,
      role="user",
      content=msg,
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

      # os.environ.unsetenv('http_proxy');
      # os.environ.unsetenv('https_proxy');

      return messages.data[0].content[0].text.value
    else:
      print("error")

      # os.environ.unsetenv('http_proxy');
      # os.environ.unsetenv('https_proxy');
      
      return ""
  
  def get_actions(self, msg):
    text = self.ask(msg)
    text = text.replace("\n", "")
    lightActions = regex.findall(r'```json({  "transitions": .*)```', text)
    print(lightActions[0])
    lightAction = []
    if len(lightActions) > 0:
      lightAction = json.loads(lightActions[0])
      print('action:', lightAction)
    return {'lightAction': lightAction}

if __name__ == "__main__":
  assistantRunner = AssistantRunner(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
  actions = assistantRunner.get_actions("这张照片中的女孩似乎正在向上看，表情可能暗示着沉思或可能的渴望。 她的嘴部放松，眼睛朝上，这可能意味着她正在思考、做白日梦，或者可能正在专注于相机视野之外的事物。 这种凝视通常意味着反思或渴望，具体取决于她正在看什么或在想什么。 她的姿势也有一定的平静，支持反思状态的想法。")
  