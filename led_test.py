import RPi.GPIO as GPIO
import time

led_pin = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)

print ("test")

for x in range(0,7) :
	GPIO.output(led_pin, True)
	time.sleep(0.2)

	GPIO.output(led_pin, False)
	time.sleep(0.2)

GPIO.cleanup()

print("end")
