import select

class EventLoop():
    def __init__(self):
        self.readers = []

    # The Event needs to have input destination
    # Can be modfied during connection period using multithreading
    def add_input(self, dest):
        self.readers.append(dest)
    
    # The Event can be run forever by calling this command until a command for exit is called
    # 
    def run_forever(self):
        while True:
            self.readers, _, _ = select.select(self.readers, [], [])
            for dest in self.readers:
                if dest is self.readers:
                    dest.on_read()