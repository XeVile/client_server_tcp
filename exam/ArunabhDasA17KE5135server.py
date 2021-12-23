import socket
import sys

# Create socket, bind, then accept.
def init_socket(host = '127.0.0.1', port = 65432):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Binding the port and showing the port used
            print(f"Binding the port {port}")
            sock.bind((host, port))
            sock.listen()
            print(f"Listening....")

            # Setting buffer size to 16 bytes
            # sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_WINDOW_CLAMP, 16)

            # Accepting connection
            conn, addr = sock.accept()
            with conn:
                print(f"Connection Established with IP | {addr[0]}:{addr[1]} |")
                
                read_cmd(conn, sock)
                

    except socket.error as msg:
        print(f"Socket Initialization failed: {str(msg)}")

# Command recv function
def read_cmd(conn, sock):
    while True:
        cmd = conn.recv(1024)
        
        if not cmd:
            sock.close()
            break

        try:
            print(repr(cmd))
            conn.sendall(b'You have connected to The SERVER')
        except socket.error as msg:
            print(f"Socket binding error: {str(msg)} \nRetrying....")
        
        if cmd == "quit" or cmd == "exit":
            conn.close()
            sock.close()
            sys.exit()
        elif len(repr(cmd)) > 0:
            client_resp = str(conn.recv(1024).decode("utf-8"))
            print(f"{client_resp}")



if __name__ == "__main__":
    init_socket()
