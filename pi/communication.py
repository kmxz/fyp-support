import requests
import time
import threading

REMOTE_HOST = 'x.ust.hk:10020'

class Communication(threading.Thread):

    def __init__(self, usss):
        self.usss = usss

    def ultrasonic_to_data(uss):
        uss.lock.acquire()
        out = uss.buf
        uss.buf = []
        uss.lock.release()
        return out

    def run(self):
        while True:
            post_data = {'time': time.time(), ultrasonic: map(ultrasonic_to_data, self.usss)}
            r = requests.post('http://' + REMOTE_HOST + '/', data=json.dumps(post_data))