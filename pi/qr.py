import subprocess
import threading
import time
import uuid
import zbar
import os

class Camera(threading.Thread):

    def __init__(self):

        super(Camera, self).__init__()
        self.fn = None
        self.lock = threading.Lock()

    def run(self):

        while True:

            fn = str(uuid.uuid4()) + '.png'

            subprocess.call(['raspistill -n -t 1 -w 256 -h 256 -o ' + fn],shell=True)

            self.lock.acquire()
            if self.fn is not None:
                os.remove(self.fn)
            self.fn = fn
            self.lock.release()

class QR(threading.Thread):

    def __init__(self):

        super(QR, self).__init__()
        self.lock = threading.Lock()
        self.buf = []
        self.camera = Camera()
        self.camera.start()

    def run(self):

        while True:

            self.camera.lock.acquire()
            fn = self.camera.fn
            self.camera.fn = None
            self.camera.lock.release()

            if fn is None:
                time.sleep(0.5)
                continue

            process = subprocess.Popen(['zbarimg -D ' + fn], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            (out, err) = process.communicate()

            os.remove(fn)

            outlines = out.splitlines()

            self.lock.acquire()
            for line in outlines:
                if line.startswith('EAN-13:'):
                    self.buf.append({'time': time.time(), 'content': out[7:]})
            self.lock.release()

