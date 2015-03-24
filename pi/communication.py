import json
import requests
import time
import threading

REMOTE_HOST = 'dmc632.resnet.ust.hk:10020'

def buffered_to_data(thread):
    thread.lock.acquire()
    out = thread.buf
    thread.buf = []
    thread.lock.release()
    return out

class Communication(threading.Thread):

    def __init__(self, usss, qr):
        super(Communication, self).__init__()
        self.usss = usss
        self.qr = qr

    def run(self):
        while True:
            last_time = time.time()
            post_data = {'time': time.time(), 'ultrasonic': map(buffered_to_data, self.usss), 'qr': buffered_to_data(self.qr)}
            r = requests.post('http://' + REMOTE_HOST + '/', data=json.dumps(post_data))
            usage = time.time() - last_time
            if (usage < 0.5):
                time.sleep(0.5 - usage)
