import os
import prediction_train.train as prediction_train

if __name__ == '__main__':
  baseDir = os.path.dirname(os.path.abspath(__file__))
  emotionList = ['happy', 'sad', 'neutral']
  sceneList = ['study', 'gaming', 'idle']

  prediction_runner = prediction_train.PredictionRunner(baseDir, emotionList, sceneList)
  # prediction_runner.train()
  prediction_runner.eval_network()

# print(baseDir)