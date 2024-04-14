import rpi.GPIO as GPIO

GPIO.setmode(GPIO.BMC)

GPIO.setup(24, GPIO.OUT)

pwm=GPIO.PWM(11, 50)

pwm.start(0)

pwm.changeDutyCycle(5)