import json
import time
import threading
import websocket

REMOTE = 'ws://pc.kmxz.net:10030/'
REMOTE_IMG = 'ws://pc.kmxz.net:10070/'

def buffered_to_data(thread):
    thread.lock.acquire()
    out = thread.buf
    thread.buf = []
    thread.lock.release()
    return out

class WsReceiver(threading.Thread):

    def __init__(self, usss, qr, pservo, switch):
        super(WsReceiver, self).__init__()
        self.ws = websocket.WebSocketApp(REMOTE,
            on_message = self.on_message
        )
        self.ws_sender = WsSender(self, usss, qr)
        self.pservo = pservo
        self.switch = switch
        self.ws.on_open = self.on_open

    def on_message(self, ws, message):
        print "Get message ", message
        loaded = json.loads(message)
        if (loaded[u'type'] == u'servo'):
            self.pservo.turn_to(loaded[u'value'])
        elif (loaded[u'type'] == u'switch'):
            self.switch.set_to(loaded[u'value'])

    def on_open(self):
        pass

    def run(self):
        self.ws_sender.start()
        while True: # loop to make sure the websocket reconnects once broken
            self.ws.run_forever()
            time.sleep(0.1) # 100 ms delay between retries

class WsSender(threading.Thread):

    def __init__(self, ws_receiver, usss, qr):
        super(WsSender, self).__init__()
        self.ws_receiver = ws_receiver
        self.usss = usss
        self.qr = qr

    def run(self):
        while True:
            last_time = time.time()
            try:
                post_data = {'time': time.time(), 'ultrasonic': map(buffered_to_data, self.usss), 'qr': buffered_to_data(self.qr), 'image': buffered_to_data(self.qr.camera)}
                self.ws_receiver.ws.send(json.dumps(post_data))
                print "Sending a message..."
            except:
                pass
            usage = time.time() - last_time
            if (usage < 0.5):
                time.sleep(0.5 - usage)
