import RPi.GPIO as GPIO


buzzer = 18
servo_pin = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)
def sound():
	pwm1 = GPIO.PWM(buzzer, 1.0)
	pwm1.start(50.0)

def opendoor() :
	pwm2 = GPIO.PWM(servo_pin, 50.0)
	pwm2.start(2.5)
	pwm2.ChangeDutyCycle(80.0)
opendoor()
sound()
GPIO.cleanup()
