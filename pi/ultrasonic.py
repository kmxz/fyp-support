import RPi.GPIO as GPIO                                 # Import GPIO library
import time                                             # Import time library
import threading                                        # Import threading library

class Ultrasonic(threading.Thread):

    def __init__(self, trig, echo):

        self.trig = trig
        self.echo = echo
        self.lock = threading.Lock()
        self.buf = []

        GPIO.setmode(GPIO.BCM)                           # Set GPIO pin numbering

        GPIO.setup(trig,GPIO.OUT)                        # Set pin as GPIO out
        GPIO.setup(echo,GPIO.IN)                         # Set pin as GPIO in

    def run(self):

        while True:

            GPIO.output(self.trig, False)                # Set TRIG as LOW
            time.sleep(0.5)                              # Delay of 0.5 seconds

            GPIO.output(self.trig, True)                 # Set TRIG as HIGH
            time.sleep(0.00001)                          # Delay of 0.00001 seconds
            GPIO.output(self.trig, False)                # Set TRIG as LOW

            while GPIO.input(self.echo)==0:              # Check whether the ECHO is LOW
                pulse_start = time.time()                # Saves the last known time of LOW pulse

            while GPIO.input(self.echo)==1:              # Check whether the ECHO is HIGH
                pulse_end = time.time()                  # Saves the last known time of HIGH pulse

            pulse_duration = pulse_end - pulse_start     # Get pulse duration to a variable

            distance = pulse_duration * 17150            # Multiply pulse duration by 17150 to get distance
            distance = round(distance, 2)                # Round to two decimal points

            self.lock.acquire()
            self.buf.append({'time': pulse_end, 'distance':distance})
            self.lock.release()