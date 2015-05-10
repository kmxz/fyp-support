import signal
from time import sleep
from RPIO import PWM
import threading
from Queue import Queue

# See documentation on http://pythonhosted.org/RPIO/pwm_py.html
servo = PWM.Servo()
signal.signal(signal.SIGCHLD, signal.SIG_IGN)

BIAS = 0.71

class Turning:

    def __init__(self, gpio):
        self.lock = threading.Lock()
        self.queue = Queue()
        self.turner = None
        self.gpio = gpio
        self.status = 0

    def transform(self, dir): # dir from -1 to 1
        rv = dir * 0.29 + BIAS
        print "[Servo in [0, 1] scale]", rv
        rv = min(max(rv, 0), 1)
        return rv

    def turn_to(self, target):
        self.lock.acquire()
        self.status = target
        servo.set_servo(self.gpio, round(self.transform(target) * 2000))
        self.lock.release()

    def add_task(self, task):
        print "[Turning task]", task
        self.queue.put(task)
        self.lock.acquire()
        if self.turner is None:
            self.turner = Turner(self)
        self.lock.release()

class Turner(threading.Thread):

    def __init__(self, turning):
        super(Turner, self).__init__()
        self.turning = turning

    def run(self):
        while not self.turning.queue.empty():
            new_status = self.turning.queue.get()
            status = self.turning.status
            if (new_status == 0) and (status > 0):
                self.right_to_center()
            elif (new_status == 0) and (status < 0):
                self.left_to_center()
            elif (status == 0) and (new_status > 0):
                self.center_to_right()
            elif (status == 0) and (new_status < 0):
                self.center_to_left()

    def center_to_left(self):
        self.pservo.turn_to(-1)
        sleep(0.2)
        self.pservo.turn_to(-0.5)

    def center_to_right(self):
        self.pservo.turn_to(1)
        sleep(0.2)
        self.pservo.turn_to(0.5)

    def left_to_center(self):
        self.pservo.turn_to(0.5)
        sleep(0.2)
        self.pservo.turn_to(0)

    def right_to_center(self):
        self.pservo.turn_to(-0.5)
        sleep(0.2)
        self.pservo.turn_to(0)