import signal
from time import sleep
from RPIO import PWM
import threading
from Queue import Queue

# See documentation on http://pythonhosted.org/RPIO/pwm_py.html
servo = PWM.Servo()
signal.signal(signal.SIGCHLD, signal.SIG_IGN)

BIAS = 0.73

class Turning:

    def __init__(self, gpio):
        self.lock = threading.Lock()
        self.queue = Queue()
        self.turner = None
        self.gpio = gpio

    def transform(self, dir): # dir from -1 to 1
        rv = dir * 0.29 + BIAS
        rrv = min(max(rv, 0), 1)
        rrv = round(rrv / 0.005) * 0.005
        print "[Servo in [0, 1] scale]", rv, " ", rrv
        return rrv

    def turn_to(self, target):
        servo.set_servo(self.gpio, int(round(self.transform(target) * 2000)))

    def add_task(self, task):
        print "[Turning task]", task
        self.queue.put(task)
        self.lock.acquire()
        if self.turner is None:
            self.turner = Turner(self)
            self.turner.start()
        self.lock.release()

class Turner(threading.Thread):

    def __init__(self, turning):
        super(Turner, self).__init__()
        self.turning = turning

    def run(self):
        while not self.turning.queue.empty():
            new_status = self.turning.queue.get()
            getattr(self, new_status)()
        self.turning.lock.acquire()
        self.turning.turner = None
        self.turning.lock.release()

    def center_to_left(self):
        self.turning.turn_to(-0.7)
        sleep(0.35)
        self.turning.turn_to(-0.3)
        sleep(1.5)

    def center_to_right(self):
        self.turning.turn_to(0.7)
        sleep(0.35)
        self.turning.turn_to(0.3)
        sleep(1.5)

    def left_to_center(self):
        self.turning.turn_to(-0.45)
        sleep(0.35)
        self.turning.turn_to(0.55)
        sleep(0.3)
        self.turning.turn_to(0)
        sleep(1.5)

    def right_to_center(self):
        self.turning.turn_to(0.45)
        sleep(0.35)
        self.turning.turn_to(-0.4)
        sleep(0.3)
        self.turning.turn_to(0)
        sleep(1.5)
