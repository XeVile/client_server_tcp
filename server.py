from datetime import datetime
import socket

# For multithreading
from _thread import *
import threading


# Thread locker
print_lock = threading.Lock()


# Response information
resp = "Calculator Mode ON \n\n Type First number \n Then Second number \n\n Lastly Choose operator: + | - | / | * \n"



# Calculator function
def calc(client):
    client.send(resp.encode("ascii"))

    while True:
        # take input for the numbers and send back response
        a = float(client.recv(1024).decode('utf-8'))
        client.send("Saved 1st".encode("ascii"))

        b = float(client.recv(1024).decode('utf-8'))
        client.send("Saved 2nd".encode("ascii"))

        # Take operator input
        op = client.recv(1024).decode('utf-8')
        
        if op == "+":
            return a + b
        elif op == "-":
            return a - b
        elif op == "/":
            return a / b
        elif op == "*":
            return a * b
        
        break

# Server programming starts here

# Function to run each new thread as requested by server initialization
# Thread function
def threaded(client):
    while True:

        # Receieved from client
        data = client.recv(1024)

        cmd = data.decode('utf-8')
        cmd = cmd.lower()

        if not data:
            print("No command received")

            print_lock.release()
            break
        
        # Exit function for client
        if cmd in ["exit", "quit"]:
            client.send(data.lower())
            print(f"Client exited")

        # Calculator function
        elif cmd in ["calc", "calculator"]:
            result = str(calc(client))
            client.send(result.encode("ascii"))
        
        elif cmd in ["today", "date", "now"]:
            client.send(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")).encode("ascii"))
        
        # Echo Uppercase for everything else
        elif len(cmd) > 0:
            client.send(data.upper())
    
    client.close()


# Initializes server
# Binds and accepts client connection requests on demand
def init_server(host = '127.0.0.1', port = 65432):
    threadCount = 0

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        # Binding the port and showing the port used
        sock.bind((host, port))
        print(f"Binding the port {port}")

        # Waiting for client to connect to server
        sock.listen()
        print(f"Listening....")

        # Setting buffer size to 16 bytes
        # sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_WINDOW_CLAMP, 16)

    except socket.error as msg:
        print(f"Socket Initialization failed: {str(msg)}")
    
    while True:
        # Accepting connection
        # First variable is the connection to client and 2nd one is address of client
        client, addr = sock.accept()

        # If connection is established with client
        # Lock the thread to the client
        print_lock.acquire()

        # Display connection message
        print(f"Connection Established with IP | {addr[0]}:{addr[1]} |")

        start_new_thread(threaded, (client,))
        threadCount += 1
    sock.close()


# Main function
if __name__ == "__main__":
    init_server()