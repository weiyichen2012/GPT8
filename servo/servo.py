import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(24, GPIO.OUT)

pwm=GPIO.PWM(24, 50)

pwm.start(0)
        
pwm.ChangeDutyCycle(7.5)
