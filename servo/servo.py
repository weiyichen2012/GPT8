import RPi.GPIO as GPIO
import os
import time
import threading
import json

class ServoRunner():
  def __init__(self, baseDir, ifDebug=True):
    self.baseDir = baseDir
    self.selfBaseDir = baseDir + "/servo/"
    self.ifDebug = ifDebug
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(24, GPIO.OUT)
    self.pwm=GPIO.PWM(24, 50)
    self.pwm.start(0)
    self.currPos = 90
    self.move(90)
  
  def smoothMoveWorker(self, degreeStart, degreeEnd, duration):
    for i in range(0, 20):
      print(i, degreeStart + (degreeEnd - degreeStart) * i / 20)
      self.move(degreeStart + (degreeEnd - degreeStart) * i / 20)
      time.sleep(duration / 20)

  def smoothMoveTo(self, degree, duration):
    print(degree, duration)
    degreeStart  = self.currPos
    degreeEnd = degree
    self.currPos = degree
    self.thread = threading.Thread(target=self.smoothMoveWorker, args=(degreeStart, degreeEnd, duration))
    self.thread.start()
    return;

  def move(self, degree):
    self.pwm.ChangeDutyCycle(2.5 + degree / 180 * 10)

  def moveByListRunner(self, degreeList, durationList):
    for i in range(0, len(degreeList)):
      if self.ifDebug:
        print("Move to: ", degreeList[i])
      self.smoothMoveTo(degreeList[i], durationList[i])
      # self.move(degreeList[i])
      time.sleep(durationList[i])
  
  def moveByListAsync(self, degreeList, durationList):
    self.thread = threading.Thread(target=self.moveByListRunner, args=(degreeList, durationList))
    self.thread.start()

  def moveByFile(self, fileName, durationList):
    # os.chdir(self.selfBaseDir)
    f = open(self.selfBaseDir + fileName, 'r')
    obj = json.loads(f.read())
    # self.moveByListRunner(obj['list'], durationList)
    self.fileThread = threading.Thread(target=self.moveByListRunner, args=(obj['list'], durationList))
    self.fileThread.start()


if __name__ == '__main__':
  servoRunner = ServoRunner(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
  # servoRunner.moveByFile('servo_waves.json')
  # time.sleep(5)
  # servoRunner.move(0)
  # time.sleep(5)
  # servoRunner.move(180)
  # time.sleep(5)

  # servoRunner.smoothMoveTo(180, 1)
  # time.sleep(1)
  # servoRunner.smoothMoveTo(0, 5)
  # time.sleep(5)
  # servoRunner.smoothMoveTo(90, 2)
  # time.sleep(2)
  # servoRunner.thread.join()
  exit(0)
