import socket
import sys

host, port, s = None, None, None

# Create socket, bind, then accept.
def init_socket(host = '127.0.0.1', port = 65432):
    global s
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
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
def socket_accept():
    global s
    con, addr = s.accept()
    print("Connection Established with IP | ", addr[0], ":", str(addr[1]), " |")
    send_cmd(con)
    con.close()

# Command sening function
def send_cmd(dest):
    while True:
        cmd = input()
        
        if cmd == "quit" or cmd == "exit":
            dest.close()
            s.close()
            sys.exit()
        elif len(str.encode(cmd)) > 0:
            dest.send(str.encode(cmd))
            client_resp = str(dest.recv(1024), "utf-8")

if __name__ = "__main__":
    init_socket()
    bind_socket()
    socket_accept()
