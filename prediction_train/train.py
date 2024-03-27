import numpy as np
import warnings
import pandas as pd
import torch
import torch.optim as optim
import os
import numpy.random as random
import time
import torch
import torch.nn as nn
import torch.nn.functional as F

img2me = lambda x, y : torch.mean((x - y) ** 2)

class NeuralNetwork(nn.Module):

    def __init__(self, input_dim, output_dim, D=5, W=200, skips=[2]):
        super().__init__()

        self.skips = skips
        self.network_linears = nn.ModuleList(
            [nn.Linear(input_dim, W)] +
            [nn.Linear(W, W) if i not in skips else nn.Linear(W + input_dim, W)
             for i in range(D - 1)]
        )

        ## output head, 2 for amplitude and phase
        self.network_output = nn.Linear(W, output_dim)

    def forward(self, network_input):
        
        x = network_input

        for i, layer in enumerate(self.network_linears):
            x = F.relu(layer(x))
            if i in self.skips:
                x = torch.cat([network_input, x], -1)

        outputs = self.network_output(x)    # (batch_size, 2)
        return outputs


emotionList = ['happy', 'sad', 'neutral']
sceneList = ['study', 'gaming', 'idle']

class PredictionNeuralRunner():
  def __init__(self, baseDir, emotionList, sceneList) -> None:
    self.baseDir = baseDir
    self.emotionList = emotionList
    self.sceneList = sceneList

    self.devices = torch.device('cpu')
    self.total_iterations = 1000
    self.PastListLen = 10
    self.input_dim = (len(self.emotionList) + len(self.sceneList)) * 10
    self.output_dim = len(self.emotionList)

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
    self.read_data()
    return
  
  def read_data(self):
    fileName = os.path.join(self.baseDir, 'input.csv')
    df = pd.read_csv(fileName)
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
        for k in range(0, len(self.emotionList)):
          if df['emotion'][currI] == self.emotionList[k]:
            self.train_input[i].append(1)
          else:
            self.train_input[i].append(0)

      for j in range(0, PastListLen):
        currI = i + j
        for k in range(0, len(self.sceneList)):
          if df['scene'][currI] == self.sceneList[k]:
            self.train_input[i].append(1)
          else:
            self.train_input[i].append(0)
      
      currI = i + 1
      self.train_label.append([])
      for k in range(0, len(self.emotionList)):
        if df['emotion'][currI] == self.emotionList[k]:
          self.train_label[i].append(1)
        else:
          self.train_label[i].append(0)

    # self.test_input = self.train_input[-testLen:]
    # self.test_label = self.train_label[-testLen:]
    self.test_input = self.train_input
    self.test_label = self.train_label      
    
    self.train_input = self.train_input[:-testLen]
    self.train_label = self.train_label[:-testLen]
      
    self.train_input = torch.tensor(self.train_input, dtype=torch.float32)
    self.train_label = torch.tensor(self.train_label, dtype=torch.float32)
    self.test_input = torch.tensor(self.test_input, dtype=torch.float32)
    self.test_label = torch.tensor(self.test_label, dtype=torch.float32)

  def load_checkpoints(self, specCkptFile=None):
    ckptsdir = os.path.join(self.baseDir, 'ckpts')
    if not os.path.exists(ckptsdir):
        os.makedirs(ckptsdir)
    ckpts = [os.path.join(ckptsdir, f) for f in sorted(os.listdir(ckptsdir)) if 'tar' in f]
    print("Found ckpts:", ckpts)

    if len(ckpts) > 0:
      if specCkptFile is not None and specCkptFile in ckpts:
        ckpt_path = os.path.join(ckptsdir, specCkptFile)
        print('Loading specific ckpt %s', ckpt_path)
      else:
        ckpt_path = ckpts[-1]
        print('Loading ckpt %s', ckpt_path)
      ckpt = torch.load(ckpt_path, map_location=self.devices)

      self.network.load_state_dict(ckpt['network_state_dict'])
      self.optimizer.load_state_dict(ckpt['optimizer_state_dict'])
      self.cosine_scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer=self.optimizer,T_max=100,eta_min=1e-6)
      self.cosine_scheduler.load_state_dict(ckpt['scheduler_state_dict'])
      self.current_iteration = ckpt['current_iteration']



  def save_checkpoint(self):
    ckptsdir = os.path.join(self.baseDir, 'ckpts')
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
    t1 = time.time()
    for i in range(0, self.total_iterations):
        if self.current_iteration > self.total_iterations:
          break
          
        result = self.network.forward(self.train_input)
        loss = img2me(result, self.train_label)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        self.cosine_scheduler.step()
        self.current_iteration += 1

        print(f"Iteration {self.current_iteration}/{self.total_iterations} loss = {loss.item()}, lr = {self.optimizer.param_groups[0]['lr']}")

        if i % 100 == 0:
            ckptname = self.save_checkpoint()
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
      print(self.emotionList[train_index], self.emotionList[actual_index], "Confidence ", result_values[train_index])
    print("Match: ", match_sum, "Mismatch: ", mismatch_sum)
  
  def predict(self, inputList):
    result = self.network.forward(inputList)
    result = result.detach().numpy()
    result_values = list(result[0])
    train_index = max(range(len(result_values)), key=result_values.__getitem__)
    print("Predicted: ", self.emotionList[train_index], "Confidence: ", result_values[train_index])
    return True, self.emotionList[train_index]

class PredictionRunner():
  def __init__(self, baseDir, emotionList, sceneList) -> None:
    self.baseDir = os.path.join(baseDir, 'prediction_train')
    self.emotionList = emotionList
    self.sceneList = sceneList

    self.runner = PredictionNeuralRunner(self.baseDir, self.emotionList, self.sceneList)
    return
  
  def train(self):
    self.runner.train()
    return
  
  def eval_network(self):
    self.runner.eval_network()
    return
  
  def predict(self, emotionList, sceneList):
    if len(emotionList) < self.runner.PastListLen or len(sceneList) < self.runner.PastListLen:
      return False, "Not enough data"
    emotionList = emotionList[-self.runner.PastListLen:]
    sceneList = sceneList[-self.runner.PastListLen:]
    inputList = []
    for i in range(0, len(emotionList)):
      for j in range(0, len(self.emotionList)):
        if emotionList[i] == self.emotionList[j]:
          inputList.append(1)
        else:
          inputList.append(0)
    
    for i in range(0, len(sceneList)):
      for j in range(0, len(self.sceneList)):
        if sceneList[i] == self.sceneList[j]:
          inputList.append(1)
        else:
          inputList.append(0)
    
    inputList = torch.tensor(inputList, dtype=torch.float32)
    result, emotion = self.runner.predict(inputList)
    return result, emotion



if __name__ == '__main__':
  warnings.simplefilter(action='ignore', category=FutureWarning)
  runner = PredictionRunner()
  # worker = PredictionNeuralRunner()
  # np.random.seed()
  # worker.train()
  # worker.eval_network()
