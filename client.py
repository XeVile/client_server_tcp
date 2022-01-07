import socket

def init_client(host = '127.0.0.1', port = 65432):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        
        while True:
            msg = input("> ")
            sock.send(msg.encode('ascii'))

            try:
                data = sock.recv(1024)
                print(f"Recieved from server: {str(data.decode('ascii'))}")
            except:
                pass

            if msg.lower() in ["exit", "quit"]:
                break
            
    except socket.error as msg:
        print("Socket Initialization failed: " + str(msg))

if __name__ == "__main__":
    init_client()