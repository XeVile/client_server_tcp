import socket
import sys

s = None

# Create socket, bind, then accept.
def init_socket(host = '127.0.0.1', port = 65432):
    global s
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                # Setting buffer size to 16 bytes
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_WINDOW_CLAMP, 16)
                
                # Binding the port and showing the port used
                print("Binding the port" + str(port))
                s.bind((host, port))
                s.listen(5)

                # Accepting connection
                conn, addr = s.accept()
                print("Connection Established with IP | ", addr[0], ":", str(addr[1]), " |")
            except socket.error as msg:
                print("Socket binding error:" + str(msg) + "\nRetrying....")
    except socket.error as msg:
        print("Socket Initialization failed:" + str(msg))
    
    # Returns the connection and address of the connection
    return conn, addr

# Establish connection with a client (Socket listening)
def send_data():
    conn, addr = init_socket()
    print("Connection Established with IP | ", addr[0], ":", str(addr[1]), " |")
    conn.close()

# Command recv function
def read_cmd(dest):
    while True:
        cmd = s.recv(1024)
        
        if cmd == "quit" or cmd == "exit":
            dest.close()
            s.close()
            sys.exit()
        elif len(str.encode(cmd)) > 0:
            dest.send(str.encode(cmd))
            client_resp = str(dest.recv(1024), "utf-8")

if __name__ == "__main__":
    conn, addr = init_socket()
    read_cmd(conn)
    conn.close()