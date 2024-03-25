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

class PredictionNeuralRunner():
  def __init__(self) -> None:
    self.devices = torch.device('cpu')
    self.total_iterations = 1000
    self.PastListLen = 10
    self.input_dim = (len(emotionList) + len(sceneList)) * 10
    self.output_dim = len(emotionList)

    self.network = NeuralNetwork(self.input_dim, self.output_dim)
    params = list(self.network.parameters())
    self.optimizer = torch.optim.Adam(params, lr=float(8e-2),
                                      weight_decay=float(5e-4),
                                      betas=(0.9, 0.999))
    self.cosine_scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer=self.optimizer,
                                                                    T_max=float(100), eta_min=float(1e-6),
                                                                    last_epoch=-1)

    self.current_iteration = 1
    self.load_checkpoints()
    self.save_freq = 100
    self.read_info()
    return
  
  def read_info(self):
    df = pd.read_csv('input.csv')
    self.train_input = []
    self.train_label = []

    testLen = 200
    self.test_input = []
    self.test_label = []

    pastEmotionList = []
    pastSceneList = []

    PastListLen = self.PastListLen

    for i in range(0, PastListLen):
      pastEmotionList.append(df['emotion'][i])
      pastSceneList.append(df['scene'][i])

    for i in range(0, len(df) - 1 - PastListLen):
      self.train_input.append([])
      for j in range(0, PastListLen):
        currI = i + j
        for k in range(0, len(emotionList)):
          if df['emotion'][currI] == emotionList[k]:
            self.train_input[i].append(1)
          else:
            self.train_input[i].append(0)

      for j in range(0, PastListLen):
        currI = i + j
        for k in range(0, len(sceneList)):
          if df['scene'][currI] == sceneList[k]:
            self.train_input[i].append(1)
          else:
            self.train_input[i].append(0)
      
      currI = i + 1
      self.train_label.append([])
      for k in range(0, len(emotionList)):
        if df['emotion'][currI] == emotionList[k]:
          self.train_label[i].append(1)
        else:
          self.train_label[i].append(0)

    self.test_input = self.train_input[-testLen:]
    self.test_label = self.train_label[-testLen:]
    self.train_input = self.train_input[:-testLen]
    self.train_label = self.train_label[:-testLen]
      
    self.train_input = torch.tensor(self.train_input, dtype=torch.float32)
    self.train_label = torch.tensor(self.train_label, dtype=torch.float32)
    self.test_input = torch.tensor(self.test_input, dtype=torch.float32)
    self.test_label = torch.tensor(self.test_label, dtype=torch.float32)

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
    t1 = time.time()
    for i in range(0, self.total_iterations):
        # with tqdm(total=self.total_iterations, desc=f"Iteration {self.current_iteration}/{self.total_iterations}") as pbar:
            # for train_input, train_label in self.train_iter:
        if self.current_iteration > self.total_iterations:
          break
          
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
        print(f"Iteration {self.current_iteration}/{self.total_iterations} loss = {loss.item()}, lr = {self.optimizer.param_groups[0]['lr']}")

        if i % 100 == 0:
            ckptname = self.save_checkpoint()
              # pbar.write('Saved checkpoints at {}'.format(ckptname))
    t2 = time.time()
    print("\nTraining take {:f} seconds. Current Iteration:{:d}, Current Loss: {:f}.\n".format(t2 - t1, self.current_iteration, loss.item()))



  def eval_network(self):
    result = self.network.forward(self.test_input)
    loss = img2me(result, self.test_label)
    print("Test Loss: ", loss.item())

    result = result.detach().numpy()
    test_label = self.test_label.detach().numpy()

    match_sum = 0
    mismatch_sum = 0
    for i in range(0, len(result)):
      result_values = list(result[i])
      train_index = max(range(len(result_values)), key=result_values.__getitem__)
      actual_values = list(test_label[i])
      actual_index = max(range(len(actual_values)), key=actual_values.__getitem__)
      if train_index != actual_index:
        mismatch_sum += 1
      else:
        match_sum += 1
      print(emotionList[train_index], emotionList[actual_index], "Confidence ", result_values[train_index])
    print("Match: ", match_sum, "Mismatch: ", mismatch_sum)

if __name__ == '__main__':
  warnings.simplefilter(action='ignore', category=FutureWarning)
  worker = PredictionNeuralRunner()
  # np.random.seed()
  # worker.train()
  worker.eval_network()
