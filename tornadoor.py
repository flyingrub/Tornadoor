#!/usr/bin/python3

import tornado.ioloop
import tornado.websocket

import string
import random

import RPi.GPIO as GPIO
import time
import os

import hashlib
import qrcode

PIN_SECRET = '9999'
CONNECTED_CLIENTS = []
SECOND = 2.0
IS_OPENING = False


class DoorWebSocket(tornado.websocket.WebSocketHandler):

    def openDoor(self):
        global IS_OPENING
        if not IS_OPENING:
            IS_OPENING = True
            print("OPEN")
            self.broadcast("door 1")
            GPIO.output(14, False)
            self.loop.add_timeout(time.time() + SECOND, self.closeDoor)
        else:
            print("ALREADY OPEN")

    def closeDoor(self):
        global IS_OPENING
        print("CLOSE")
        self.broadcast("door 0")
        GPIO.output(14, True)
        IS_OPENING = False

    def open(self):
        self.loop = tornado.ioloop.IOLoop.instance()
        print("WebSocket opened")
        CONNECTED_CLIENTS.append(self)

    def on_message(self, message):
        print(">" + message)
        if "hello" in message:
            self.sendAlea()
        elif "open" in message:
            self.onOpenRequest(message)

    def on_close(self):
        print("WebSocket closed")
        CONNECTED_CLIENTS.remove(self)

    def sendAlea(self):
        self.cur_alea = ''.join(
                            random.SystemRandom().choice(
                                string.ascii_uppercase + string.digits
                            ) for _ in range(10)
                        )
        self.write_message("alea " + self.cur_alea)

    def onOpenRequest(self, payload):
        data = payload.split(' ')
        alea = data[0]
        pin = data[2]

        if alea == self.cur_alea:
            if pin == PIN_SECRET:
                self.openDoor()
            else:
                print("Acces Denied: Wrong pin")
        else:
            print("Access Denied: Wrong Alea")

    def broadcast(self, msg):
        for c in CONNECTED_CLIENTS:
            c.write_message(msg)

app = tornado.web.Application([
    (r'/dooritos/', DoorWebSocket),
])

if __name__ == "__main__":
    os.chdir("/root/tornadoor")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(14, GPIO.OUT)
    GPIO.output(14, True)
    app.listen(8888, "192.168.1.99", ssl_options={
        "certfile": "server.crt",
        "keyfile": "server.key",
    })

    h = hashlib.sha1()
    with open('server.crt', 'rb') as crt:
        h.update(crt.read())
    cert_hash = h.hexdigest()
    print(cert_hash)
    img = qrcode.make(cert_hash)
    img.save("certify.png")

    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print("Goodbye!")
    finally:
        GPIO.output(14, True)
        GPIO.cleanup()
