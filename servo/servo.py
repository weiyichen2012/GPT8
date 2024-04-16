import RPi.GPIO as GPIO
import os
import time
import threading

class ServoRunner():
  def __init__(self, baseDir):
    self.baseDir = baseDir
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(24, GPIO.OUT)
    self.pwm=GPIO.PWM(24, 50)
    self.pwm.start(0)
    self.currPos = 90
    self.move(90)
  
  def smoothMoveWorker(self, degreeStart, degreeEnd, duration):
    durationMs = int(duration * 1000)
    for i in range(0, int(durationMs / 100)):
      print(i, degreeStart + (degreeEnd - degreeStart) * i / (durationMs / 100))
      self.move(degreeStart + (degreeEnd - degreeStart) * i / (durationMs / 100))
      time.sleep(100)

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

if __name__ == '__main__':
  servoRunner = ServoRunner(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
  # servoRunner.move(0)
  # time.sleep(1)
  # servoRunner.move(180)
  servoRunner.smoothMoveTo(180, 1)
  time.sleep(1)
  servoRunner.smoothMoveTo(0, 5)
  time.sleep(5)
  servoRunner.smoothMoveTo(90, 2)
  time.sleep(2)
  servoRunner.thread.join()
  exit(0)
