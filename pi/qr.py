import subprocess
import threading
import time
import uuid
import zbar

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

        last_fn = None

        while True:

            self.camera.lock.acquire()
            fn = self.camera.fn
            self.camera.lock.release()

            if fn == last_fn:
                time.sleep(0.5)
                continue
            last_fn = fn

            process = subprocess.Popen(['zbarimg -D ' + fn], stdout=subprocess.PIPE, shell=True)
            (out, err) = process.communicate()

            outlines = out.splitlines()

            self.lock.acquire()
            for line in outlines:
                if line.startswith('QR-Code:'):
                    self.buf.append({'time': time.time(), 'content': out[8:]})
            self.lock.release()
