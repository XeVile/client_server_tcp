import socket
import select
import sys

class Connection():
    def __init__(self):
        self.sock = socket.socket()
        self.sock.connect(("localhost", 65432))
    def fileno(self):
        return self.sock.fileno()
    def on_read(self):
        msg = self.sock.recv(1000).decode("utf-8")
        print(msg)
    def send(self, msg):
        self.sock.send(msg)

class Input():
    def __init__(self, sender):
        self.sender = sender
    def fileno():
        return sys.stdin.fileno()
    def on_read(self):
        msg = sys.stdin.readline()
        self.sender.send(msg)

class EventLoop():
    readers = []
    def __init__(self):
        pass

    # The Event needs to have input destination
    # Can be modfied during connection period using multithreading
    def add_input(self, dest):
        self.readers.append(dest)
        print(f'{self.readers}')
    
    # The Event can be run forever by calling this command until a command for exit is called
    # 
    def run_forever(self):
        while True:
            self.readers, _, _ = select.select(self.readers, [], [])
            for dest in self.readers:
                if dest is self.readers:
                    print(f"{dest}")
                    dest.on_read()


if __name__ == "__main__":
    feed = Connection()
    in_reader = Input(feed)
    eventio = EventLoop()
    eventio.add_input(feed)
    eventio.add_input(in_reader)