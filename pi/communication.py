import json
import time
import threading
import websocket

REMOTE = 'ws://pc.kmxz.net:10030/'

def buffered_to_data(thread):
    thread.lock.acquire()
    out = thread.buf
    thread.buf = []
    thread.lock.release()
    return out

class Communication(threading.Thread):

    def __init__(self, usss, qr, pservo):
        super(Communication, self).__init__()
        self.usss = usss
        self.qr = qr
        self.pservo = pservo
        self.ws = websocket.WebSocketApp(REMOTE,
            on_message = on_message
        )
        self.ws.on_open = self.on_open

    def on_message(self, ws, message):
        self.pservo.turn_to(float(message))

    def on_open(self, ws):
        while True:
            last_time = time.time()
            post_data = {'time': time.time(), 'ultrasonic': map(buffered_to_data, self.usss), 'qr': buffered_to_data(self.qr)}
            ws.send(json.dumps(post_data))
            usage = time.time() - last_time
            if (usage < 0.5):
                time.sleep(0.5 - usage)

    def run(self):
        self.ws.run_forever()

