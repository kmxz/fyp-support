import RPi.GPIO as GPIO

class Switch:

    def __init__(self, gpio):
        self.gpio = gpio
        GPIO.setup(gpio, GPIO.OUT)

    def set_to(self, target):
        GPIO.output(self.gpio, target)
