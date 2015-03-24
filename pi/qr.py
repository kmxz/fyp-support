import subprocess
import threading
import time
import uuid
import zbar

class Camera(threading.Thread):

    def __init__(self):

        self.fn = None
        self.lock = threading.Lock()

    def run(self):

        while True:

            fn = str(uuid.uuid4()) + '.png'

            subprocess.call(['raspistill -n -t 1 -w 256 -h 256 -o ' + fn],shell=True)

            self.lock.acquire()
            self.fn = fn
            self.lock.release()

camera = Camera()

class QR(threading.Thread):

    def __init__(self):

        self.lock = threading.Lock()
        self.buf = []
        self.last_fn = None
        self.last_qr = None

    def run(self):

        while True:

            camera.lock.acquire()
            fn = camera.fn
            camera.lock.release()

            if fn == self.last_fn:
                time.sleep(0.5)
                continue
            self.last_fn = fn

            process = subprocess.Popen(['zbarimg -D ' + fn], stdout=subprocess.PIPE, shell=True)
            (out, err) = process.communicate()

            outlines = out.splitlines()

            self.lock.acquire()
            for line in outlines:
                if line.startswith('QR-Code:'):
                    self.buf.append({'time': time.time(), 'content': out[8:]})
            self.lock.release()