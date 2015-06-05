#!/usr/bin/python
from tornado.ioloop import IOLoop
from tornado.websocket import websocket_connect


if __name__ == "__main__":
    ws = websocket_connect("wss://192.168.1.99:8888")
    IOLoop.instance().start()
