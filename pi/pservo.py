import signal
import threading
import time
from RPIO import PWM

# See documentation on http://pythonhosted.org/RPIO/pwm_py.html
servo = PWM.Servo()
signal.signal(signal.SIGCHLD, signal.SIG_IGN)

class PServo:

    def __init__(self, gpio):
        self.gpio = gpio

    def turn_to(self, target):
        servo.set_servo(self.gpio, target * 2000)
