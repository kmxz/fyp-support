import signal
import threading
import time
from RPIO import PWM

# See documentation on http://pythonhosted.org/RPIO/pwm_py.html
servo = PWM.Servo()
signal.signal(signal.SIGCHLD, signal.SIG_IGN)

class PServo(threading.Thread):

    def __init__(self, gpio):
        super(PServo, self).__init__()
        self.gpio = gpio

    def run(self):
        while True:
            servo.set_servo(self.gpio, 400)
            time.sleep(0.75)
            servo.set_servo(self.gpio, 800)
            time.sleep(0.75)
            servo.set_servo(self.gpio, 1200)
            time.sleep(0.75)
            servo.set_servo(self.gpio, 1600)
            time.sleep(0.75)
