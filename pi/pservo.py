import signal
from RPIO import PWM

# See documentation on http://pythonhosted.org/RPIO/pwm_py.html
servo = PWM.Servo()
signal.signal(signal.SIGCHLD, signal.SIG_IGN)

class PServo:

    def __init__(self, gpio):
        self.gpio = gpio

    def transform(self, dir): # dir from -1 to 1
        return dir * 0.29 + 0.71

    def turn_to(self, target):
        servo.set_servo(self.gpio, self.transform(target) * 2000)
