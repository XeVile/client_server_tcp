import socket
import select
import sys

class Connection():
    def __init__(self):
        self.s = socket.socket()
        self.s.connect(("localhost", 1234))
    def fileno(self):
        return self.s.fileno()
    def on_read(self):
        msg = self.s.recv(1000).decode("utf-8")
        print(msg)
    def send(self, msg):
        self.s.send(msg)

class Input():
    def __init__(self, sender):
        self.sender = sender
    def fileno():
        return sys.stdin.fileno()
    def on_read(self):
        msg = sys.stdin.readline()
        self.sender.send(msg)

class EventLoop():
    def __init__(self, reader):
        self.readers = []
    def add_reader(self, reader):
        self.readers.append(reader)
    def run_forever(self):
        while True:
            self.readers, _, _ = select.select(self.readers, [], [])
            for reader in self.readers:
                if reader is connection:
                    reader.on_read()

connection = Connection()
in_reader = Input(connection)

eventio = EventLoop()
eventio.add_reader(connection)
eventio.add_reader(in_reader)
eventio.run_forever()