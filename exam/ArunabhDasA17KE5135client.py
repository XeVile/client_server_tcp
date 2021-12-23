import socket
import sys

# Create socket, bind, then accept.
def init_client(host = '127.0.0.1', port = 65432):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
            sock.sendall(b'I am a network programmer in Red Circle Sdn. Bhd')

            send_cmd(sock)
            while True:
                msg = input("> ")
                sock.send(msg.encode('utf8'))

            try:
                data = sock.recv(1024)
            except socket.error as msg:
                print(f"Connection error: {str(msg)} \nRetrying....")
            
    except socket.error as msg:
        print("Socket Initialization failed: " + str(msg))

# Command sening function
def send_cmd(sock):
    while True:
        cmd = input()
        
        if cmd == "quit" or cmd == "exit":
            sock.close()
            sys.exit()
        elif len(str.encode(cmd)) > 0:
            sock.send(str.encode(cmd))
            client_resp = str(sock.recv(1024), "utf-8")

if __name__ == "__main__":
    init_client()