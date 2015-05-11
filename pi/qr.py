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

    def get_fn(self, c):

        return self.prefix + '_' + str(c) + '.jpg'

    def run(self):

        self.prefix = str(uuid.uuid4())
        self.fastcamd = subprocess.Popen(['raspifastcamd', '-w' , '128', '-h', '256', '-o', self.prefix + '_%d.jpg'], cwd='/tmp')

        time.sleep(0.5) # this is really hacky

        while True:
            self.fastcamd.send_signal(signal.SIGUSR1)

            tmp_fn = '/tmp/' + self.get_fn(self.c + 1)

            while not os.path.isfile(tmp_fn):
                time.sleep(0.05)

            self.c = self.c + 1

class Program:

    def __init__(self, switch, turning):

        self.lock = threading.Lock()
        self.buf = []
        self.switch = switch
        self.turning = turning
        self.stage = 0

    def on_barcode(self, content):

        if ("1024" in content) and (self.stage == 0):
            self.lock.acquire()
            self.buf.append({'time': time.time(), 'content': "Command 1024"})
            self.lock.release()
            self.stage = 1
            self.switch.set_to(False)
            self.turning.add_task('center_to_left')
            self.switch.set_to(True)

        elif ("2048" in content) and (self.stage == 1):
            self.lock.acquire()
            self.buf.append({'time': time.time(), 'content': "Command 2048"})
            self.lock.release()
            self.stage = 2
            self.switch.set_to(False)
            self.turning.add_task('center_to_left')
            self.switch.set_to(True)

class QR(threading.Thread):

    def __init__(self, program):

        super(QR, self).__init__()
        self.lock = threading.Lock()
        self.buf = []
        self.last_c = -1
        self.camera = Camera()
        self.camera.start()
        self.program = program

    def run(self):

        while True:
            if self.camera.c < 0:
                print "[QR] ~ No picture available yet..."
                time.sleep(0.1)
                continue
            elif self.camera.c <= self.last_c:
                print "[QR] - Old picture..."
                time.sleep(0.1)
                continue
            elif self.camera.c > self.last_c + 1:
                print "[QR] + Skipped picture..."
            else:
                print "[QR] * Normal"

            fn = self.camera.get_fn(self.camera.c)
            self.last_c = self.camera.c

            process = subprocess.Popen(['zbarimg -Sdis -Sean13.en -D '+ fn], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd='/tmp')
            (out, err) = process.communicate()

            outlines = out.splitlines()

            self.lock.acquire()
            for line in outlines:
                if line.startswith('EAN-13:'):
                    self.buf.append({'time': time.time(), 'content': line[7:]})
                    self.program.on_barcode(line[7:])
            self.lock.release()

