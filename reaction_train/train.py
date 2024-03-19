import numpy as np
import warnings
from model import *
import pandas as pd
import torch
import torch.optim as optim
import os
# from tqdm import tqdm
import numpy.random as random
import time

emotionList = ['happy', 'sad', 'neutral']
sceneList = ['study', 'gaming', 'idle']

actionList = ['keep_still', 'pat_pat', 'dance', 'sing']
lightList = ['red', 'blue', 'white', 'yellow']

class NeuralRunner():
  def __init__(self) -> None:
    self.devices = torch.device('cpu')
    self.total_iterations = 1000
    self.input_dim = len(emotionList) + len(sceneList)
    self.output_dim = len(actionList) + len(lightList)

    self.network = NeuralNetwork(self.input_dim, self.output_dim)
    params = list(self.network.parameters())
    self.optimizer = torch.optim.Adam(params, lr=float(8e-2),
                                      weight_decay=float(5e-4),
                                      betas=(0.9, 0.999))
    self.cosine_scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer=self.optimizer,
                                                                    T_max=float(50), eta_min=float(1e-6),
                                                                    last_epoch=-1)

    self.current_iteration = 1
    self.load_checkpoints()
    self.save_freq = 100
    return
  
  def read_info(self):
    df = pd.read_csv('input.csv')
    self.train_input = []
    self.train_label = []

    for i in range(0, len(df)):
      self.train_input.append([])
      for j in range(0, len(emotionList)):
        if df['emotion'][i] == emotionList[j]:
          self.train_input[i].append(1)
        else:
          self.train_input[i].append(0)

      for j in range(0, len(sceneList)):
        if df['scene'][i] == sceneList[j]:
          self.train_input[i].append(1)
        else:
          self.train_input[i].append(0)
        
      self.train_label.append([])
      for j in range(0, len(actionList)):
        if df['action'][i] == actionList[j]:
          self.train_label[i].append(df['preference'][i])
        else:
          self.train_label[i].append(0)
        
      for j in range(0, len(lightList)):
        if df['light'][i] == lightList[j]:
          self.train_label[i].append(df['preference'][i])
        else:
          self.train_label[i].append(0)
    
    self.train_input = torch.tensor(self.train_input, dtype=torch.float32)
    self.train_label = torch.tensor(self.train_label, dtype=torch.float32)

  def add_info(self, emotion, scene, action, light, preference):
    if not os.path.exists('input.csv'):
      df = pd.DataFrame(columns=['emotion', 'scene', 'action', 'light', 'preference'])
      df.to_csv('input.csv', index=False)
    df = pd.read_csv('input.csv')
    df = pd.concat([df, pd.DataFrame({'emotion': emotion, 'scene': scene, 'action': action, 'light': light, 'preference': preference}, index=[0])])
    df.to_csv('input.csv', index=False)
    return

  def load_checkpoints(self):
    ckptsdir = os.path.join('ckpts')
    if not os.path.exists(ckptsdir):
        os.makedirs(ckptsdir)
    ckpts = [os.path.join(ckptsdir, f) for f in sorted(os.listdir(ckptsdir)) if 'tar' in f]
    print("Found ckpts:", ckpts)

    if len(ckpts) > 0:
      ckpt_path = ckpts[-1]
      print('Loading ckpt %s', ckpt_path)
      ckpt = torch.load(ckpt_path, map_location=self.devices)

      self.network.load_state_dict(ckpt['network_state_dict'])
      self.optimizer.load_state_dict(ckpt['optimizer_state_dict'])
      self.cosine_scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer=self.optimizer,T_max=100,eta_min=1e-6)
      self.cosine_scheduler.load_state_dict(ckpt['scheduler_state_dict'])
      self.current_iteration = ckpt['current_iteration']



  def save_checkpoint(self):
    ckptsdir = os.path.join('ckpts')
    model_lst = [x for x in sorted(os.listdir(ckptsdir)) if x.endswith('.tar')]
    if len(model_lst) > 2:
      os.remove(ckptsdir + '/%s' % model_lst[0])

    ckptname = os.path.join(ckptsdir, '{:06d}.tar'.format(self.current_iteration))
    torch.save({
        'current_iteration': self.current_iteration,
        'network_state_dict': self.network.state_dict(),
        'optimizer_state_dict': self.optimizer.state_dict(),
        'scheduler_state_dict': self.cosine_scheduler.state_dict()
    }, ckptname)
    print('Saved checkpoints at %s', ckptname)
    return ckptname



  def train(self):
    # print("Start training. Current Iteration:%d", self.current_iteration)
    if self.current_iteration == 1:
      i_range = 50
    else:
      i_range = 100

    t1 = time.time()
    for i in range(0, i_range):
        # with tqdm(total=self.total_iterations, desc=f"Iteration {self.current_iteration}/{self.total_iterations}") as pbar:
            # for train_input, train_label in self.train_iter:
          # if self.current_iteration > self.total_iterations:
          #     break
          
        result = self.network.forward(self.train_input)
        loss = img2me(result, self.train_label)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        self.cosine_scheduler.step()
        self.current_iteration += 1

          # self.writer.add_scalar('Loss/loss', loss, self.current_iteration)
          # pbar.update(1)
          # pbar.set_description(f"Iteration {self.current_iteration}/{self.total_iterations}")
          # pbar.set_postfix_str('loss = {:.6f}, lr = {:.6f}'.format(loss.item(), self.optimizer.param_groups[0]['lr']))
          # print(f"Iteration {self.current_iteration}/{self.total_iterations} loss = {loss.item()}, lr = {self.optimizer.param_groups[0]['lr']}")

        if i == 99:
            ckptname = self.save_checkpoint()
              # pbar.write('Saved checkpoints at {}'.format(ckptname))
    t2 = time.time()
    print("\nTraining take {:f} seconds. Current Iteration:{:d}, Current Loss: {:f}.\n".format(t2 - t1, self.current_iteration, loss.item()))



  def eval_network(self, emotion, scene, ifSomeRandom = False):
    i = 0
    self.train_input = [[]]
    for j in range(0, len(emotionList)):
      if emotion == emotionList[j]:
          self.train_input[i].append(1)
      else:
          self.train_input[i].append(0)
      
    for j in range(0, len(sceneList)):
      if scene == sceneList[j]:
          self.train_input[i].append(1)
      else:
          self.train_input[i].append(0)

    self.train_input = torch.tensor(self.train_input, dtype=torch.float32)
    result = self.network.forward(self.train_input)
    result = result.detach().numpy()

    action = actionList[result[0][0: len(actionList)].argmax()]
    light = lightList[result[0][len(actionList):].argmax()]

    if np.random.rand() < 0.2 and ifSomeRandom:
      action = random.choice(actionList)
      light = random.choice(lightList)
      print("This is random Response")
    
    return action, light

      

if __name__ == '__main__':
  warnings.simplefilter(action='ignore', category=FutureWarning)
  worker = NeuralRunner()
  np.random.seed()
#   worker.train()
#   worker.eval_network()
  while True:
    emotion = random.choice(emotionList)
    scene = random.choice(sceneList)
    action, light = worker.eval_network(emotion, scene, ifSomeRandom=True)

    print("When you are " + emotion + " and " + scene + ' it ' + action + ' and ' + light)
    preference = float(input('preference(from -1 to 1, -1: dislike, 0: neutral 1: like): '))
    worker.add_info(emotion, scene, action, light, preference)
    worker.read_info()
    worker.train()