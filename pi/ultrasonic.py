import RPi.GPIO as GPIO
import time
import threading

class Ultrasonic(threading.Thread):

    def __init__(self, trig, echo):

        super(Ultrasonic, self).__init__()

        self.trig = trig
        self.echo = echo
        self.lock = threading.Lock()
        self.buf = []

        GPIO.setup(trig, GPIO.OUT)
        GPIO.setup(echo, GPIO.IN)

    def run(self):

        while True:
            result = self.get_dist()
            if (result < 0): # no result, time-out instead
                continue
            self.lock.acquire()
            self.buf.append({'time': time.time(), 'distance': result})
            self.lock.release()

    def get_dist(self):

        trip_start = time.time()

        GPIO.output(self.trig, False) # set TRIG as LOW
        time.sleep(0.25) # delay of 0.25 seconds to let get rest

        GPIO.output(self.trig, True) # set TRIG as HIGH
        time.sleep(0.00001) # delay of 0.00001 seconds
        GPIO.output(self.trig, False) # set TRIG as LOW

        while GPIO.input(self.echo)==0: # check whether the ECHO is LOW
            pulse_start = time.time() # saves the last known time of LOW pulse
            if ((pulse_start - trip_start) > 0.05):
                return -1

        while GPIO.input(self.echo)==1: # check whether the ECHO is HIGH
            pulse_end = time.time() # saves the last known time of HIGH pulse
            pulse_duration = pulse_end - pulse_start # get pulse duration to a variable
            if (pulse_duration > 0.05):
                return -1

        distance = pulse_duration * 17150 # multiply pulse duration by 17150 to get distance
        return round(distance, 2) # round to two decimal points
