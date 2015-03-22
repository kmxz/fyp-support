import threading
import time
import zbar

class QR(threading.Thread):

    def __init__(self):

        self.lock = threading.Lock()
        self.buf = []
        self.last_qr = None

        # create a Processor
        self.proc = zbar.Processor()

        # configure the Processor
        self.proc.parse_config('enable')

        # initialize the Processor
        self.proc.init('/dev/video0')

    def run(self):

        # enable the preview window
        self.proc.visible = True

        while True:

            # read at least one barcode (or until window closed)
            self.proc.process_one()

            self.lock.acquire()

            for symbol in self.proc.results:
                print self.buf.append({'time': time.time(), 'content': symbol.data})

            self.lock.release()