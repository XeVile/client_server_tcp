import socket
import sys

from eventloop import EventLoop

class Connection():
    def __init__(self):
        self.sock = socket.socket()
        self.sock.connect(("localhost", 65432))
    def fileno(self):
        return self.sock.fileno()
    def on_read(self):
        msg = self.sock.recv(1000).decode("utf8")
        print(msg)
    def send(self, msg):
        self.sock.send(msg)

class Input():
    def __init__(self, sender):
        self.sender = sender
    def fileno():
        return sys.stdin.fileno()
    def on_read(self):
        msg = sys.stdin.readline().encode("utf8")
        self.sender.send(msg)

if __name__ == "__main__":
    feed = Connection()
    in_reader = Input(feed)
    eventio = EventLoop()
    eventio.add_input(feed)
    eventio.add_input(in_reader)
    eventio.run_forever()