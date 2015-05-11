import subprocess
import threading
import time
import uuid
import os
import signal

class Camera(threading.Thread):

    def __init__(self):

        super(Camera, self).__init__()

        self.sender = None
        self.fastcamd = None
        self.c = -1
        self.prefix = None

        self.time = time.time()

    def get_fn(self, c):

        return self.prefix + '_' + str(c) + '.jpg'

    def run(self):

        self.comm.start()
        self.prefix = str(uuid.uuid4())
        self.fastcamd = subprocess.Popen(['raspifastcamd', '-w', '128', '-h', '256', '-o', self.prefix + '_%d.jpg'], cwd='/tmp')

        time.sleep(1) # this is really hacky

        while True:
            self.fastcamd.send_signal(signal.SIGUSR1)

            tmp_fn = '/tmp/' + self.get_fn(self.c + 1)

            while not os.path.isfile(tmp_fn):
                time.sleep(0.1)

            self.c = self.c + 1

            print "[CAMERA SINCE ", self.c , "]" , (time.time() - self.time)

class QR(threading.Thread):

    def __init__(self, switch):

        super(QR, self).__init__()
        self.lock = threading.Lock()
        self.buf = []
        self.switch = switch
        self.last_c = -1
        self.camera = Camera()
        self.camera.start()

    def on_barcode(self, content):

        self.switch.set_to(False)

    def run(self):

        while True:
            print "[BARCODE]"

            if self.camera.c <= self.last_c:
                time.sleep(0.2)
                print "[QR] Old picture..."
                continue
            elif self.camera.c < 0:
                print "[QR] No picture available yet..."
                time.sleep(0.2)
                continue

            fn = self.camera.get_fn(self.camera.c)
            self.last_c = self.camera.c

            process = subprocess.Popen(['zbarimg -D ' + fn], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd='/tmp')
            (out, err) = process.communicate()

            outlines = out.splitlines()

            self.lock.acquire()
            for line in outlines:
                if line.startswith('EAN-13:'):
                    self.buf.append({'time': time.time(), 'content': line[7:]})
                    self.on_barcode(line[7:])
            self.lock.release()

