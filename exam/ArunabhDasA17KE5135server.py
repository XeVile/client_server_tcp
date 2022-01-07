import socket
import sys
import datetime

conn_status = "Off"

# Create socket, bind, then accept.
def init_socket(host = '127.0.0.1', port = 65432):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Binding the port and showing the port used
            print(f"Binding the port {port}")

            sock.bind((host, port))

            # Waiting for client to connect to server
            sock.listen()

            print(f"Listening....")

            # Setting buffer size to 16 bytes
            # sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_WINDOW_CLAMP, 16)

            # Accepting connection
            # First variable is the connection to client and 2nd one is address of client
            conn, addr = sock.accept()

            # If connection is extablished with client
            with conn:
                print(f"Connection Established with IP | {addr[0]}:{addr[1]} |")

                read_cmd(conn, addr)
                send_cmd(conn, "Test")
                return conn, addr

    except socket.error as msg:
        print(f"Socket Initialization failed: {str(msg)}")


def send_cmd(conn, msg):
    while True:
        conn.send(msg.encode())

        if not msg:
            break

# Command recv function
def read_cmd(conn, sock):
    while True:
        try:
            send_cmd(conn, 'You have connected to The SERVER')
        except socket.error as msg:
            print(f"Socket binding error: {str(msg)} \nRetrying....")

        cmd = conn.recv(1024)
        
        if not cmd:
            break
        
        if repr(cmd) == "quit" or cmd == "exit":
            break
        elif len(repr(cmd)) > 0:
            print(f"{cmd}")
    
    conn.close()
    sock.close()
    sys.exit()


def capitalize(cmd):
    return cmd.upper()

def calculator(cmd):
    return 


if __name__ == "__main__":
    conn, addr = init_socket()