# Multi-threading
import weave
import server
import sys

# Thread locker
comms_thread = weave.StoppableThread()

# Main function
if __name__ == "__main__":
    sv = server.server(thread=comms_thread)
    sock = sv.create()
    
    sv.allow_conns(sock)

    while not comms_thread.stopped():
        print("stopping...")
        comms_thread.stop()
        sv.kill(sock)
        sock.close()
        
        if comms_thread.stopped():
            sys.exit()
            break