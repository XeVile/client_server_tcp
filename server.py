from datetime import datetime
import socket

# For updating the SQL
import db_func as db
from pathlib import Path


database = str(Path.cwd()) + "/protected.db"

# Response information
options = "\n\n\tList of possible options:\n\t\t\
                > Calc\n\t\t\
                > Stat\n\t\t\
                > Now\n\t\t\
                > Chat\n\t\t\
                > Help\n\t\t\
                > @Quit to Kill Server!\n\
                Can also try other text\n"
welcomeResp = "\nWelcome! You are connected to Divoc V2" + options

stat = None

# Global variables for access
conn_List = []
addr_List = []


# Server Function class
class server_func:
    global options
    
    def __init__(self, conn, data, db_conn):
        self.conn = conn
        self.cmd = data.decode('utf-8').lower()
        self.db_conn = db_conn
    
    def __send(self, msg):
        self.conn.send(msg.encode("utf-8"))
    
    def __recv(self):
        return self.conn.recv(1024).decode("utf-8")

    def __calc(self, client_id):
        """Calculation Mode: A function that calculates decimal numbers and sends results\n\n
        Handles input exceptions"""

        defaultMsg = "\n====== CALCULATION MODE ======\n\nSteps of usage\
            \n\n\t>> Input X \n\t>> Input Y \n\n\t>> Input Operator: + | - | / | * \n"
        
        db.create_comms_archive(self.db_conn, (client_id,"Calculation Mode", "-",str(datetime.now().strftime("%H:%M:%S"))))
        # Function starts -----
        self.__send(defaultMsg)

        while True:
            # take input for the numbers and send back response
            try:
                a = float(self.__recv())
                db.create_comms_archive(self.db_conn, (client_id,"-", str(a),str(datetime.now().strftime("%H:%M:%S"))))
                aMsg = "X = " + str(int(a))
                self.__send(aMsg)
                db.create_comms_archive(self.db_conn, (client_id, str(b),"-",str(datetime.now().strftime("%H:%M:%S"))))

                b = float(self.__recv())
                db.create_comms_archive(self.db_conn, (client_id,"-", str(b),str(datetime.now().strftime("%H:%M:%S"))))
                bMsg = "Y = " + str(int(b))
                self.__send(bMsg)
                db.create_comms_archive(self.db_conn, (client_id, str(bMsg),"-",str(datetime.now().strftime("%H:%M:%S"))))

                # Take operator input
                op = self.__recv()
                db.create_comms_archive(self.db_conn, (client_id,"-", str(op),str(datetime.now().strftime("%H:%M:%S"))))
                
                if op == "+":
                    result = str(a + b)
                elif op == "-":
                    result = str(a - b)
                elif op == "/":
                    result = str(a / b)
                elif op == "*":
                    result = str(a * b)
                
                self.__send(result)
                db.create_comms_archive(self.db_conn, (client_id, str(result),"-",str(datetime.now().strftime("%H:%M:%S"))))
                break

            except:
                # I SEE YOU, I KNOW WHAT YOU ARE TRYING
                # (ὸ_ό) BAD!
                self.__send("Try DECIMAL number for input!\nGo back to CALCULATION MODE?\n\
                    Type Y/N, anything else will exit mode: ")
                db.create_comms_archive(self.db_conn, (client_id, "Error: Not decimal number, read steps","-",str(datetime.now().strftime("%H:%M:%S"))))
                
                choice = self.__recv()
                if choice.lower() in ["y", "yes"]:
                    self.__send(defaultMsg)
                else:
                    self.__send("Exited CALCULATION MODE")
                    db.create_comms_archive(self.db_conn, (client_id,"Exited Calc mode", "-",str(datetime.now().strftime("%H:%M:%S"))))
                    break
    
    def __switch(self, client_id):
        """Allows status validation of a boolean"""

        global stat
        defaultMsg = "\n====== STATUS VALIDATION ======\n\n\t"

        if stat:
            onMsg = "STATUS: Currently ON\n\nChange Status? Y/N\n"
            statusMsg = defaultMsg + onMsg
            db.create_comms_archive(self.db_conn, (client_id, statusMsg,"-",str(datetime.now().strftime("%H:%M:%S"))))
            self.__send(statusMsg)
        else:
            offMsg = "STATUS: Currently OFF\n\nChange Status? Y/N\n"
            statusMsg = defaultMsg + offMsg
            db.create_comms_archive(self.db_conn, (client_id, statusMsg,"-",str(datetime.now().strftime("%H:%M:%S"))))
            self.__send(statusMsg)
        
        choice = self.__recv()
        db.create_comms_archive(self.db_conn, (client_id,"-", str(choice),str(datetime.now().strftime("%H:%M:%S"))))

        if choice.lower() in ["y", "yes"]:
            stat = not stat
            print(stat)
            if stat == True:
                self.__send("Status Changed to ON")
                db.create_comms_archive(self.db_conn, (client_id, "Status Changed to ON","-",str(datetime.now().strftime("%H:%M:%S"))))
            else:
                self.__send("Status Changed to OFF")
                db.create_comms_archive(self.db_conn, (client_id, "Status Changed to Off","-",str(datetime.now().strftime("%H:%M:%S"))))
        else:
            self.__send("Going back to OPTIONS selection")

    def select(self, client_id):
        if self.cmd in ["calc", "calculator"]:
            self.__calc(client_id)
        
        # Check current datetime
        elif self.cmd in ["today", "date", "now"]:
            self.__send(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        
        # Status toggling
        elif self.cmd in ["stat", "status"]:
            self.__switch(client_id)

        # Show options
        elif self.cmd in ["options", "opt", "help"]:
            self.__send(options)
        
        # Echo Uppercase for everything else
        elif len(self.cmd) > 0:
            self.__send(self.cmd.upper())
            db.create_comms_archive(self.db_conn, (client_id, str(self.cmd.upper()),"-",str(datetime.now().strftime("%H:%M:%S"))))



# Server programming starts here

# Function to run each new thread as requested by server initialization
# Thread function


class server:
    """A server class that can create, bind and accept connections\n
        Initialize server using host, port and thread (Must have)
        Default: 127.0.0.1 (HOST), 65432 (PORT)
        1) create() -> Make socket and listen
        2) allow_connects() -> Accept an incoming connection and send response
        3) """

    def __init__(self, host = '127.0.0.1', port = 65432, thread = None):
        self.__host = host
        self.__port = port
        self.__kill = False
        self.__timeout = False
        self.__thread= thread
        self.numOfConn = 0
    
    def __timeout__(self, sock):
        if self.numOfConn == 0 & self.__timeout == False:
            print('y')
            self.__timeout = True
            sock.settimeout(5.0)
        elif self.numOfConn > 0:
            print('x')
            self.__timeout = False
            sock.settimeout(300.0)

    def create(self):
        """Create and bind socket to the initialized Server host and port.\
        This bound socket can be used to start allowing connections to the server.\n\n\
        A Socket object is returned\n\n\
        If the host and\or port are already being used None object is returned"""

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
            # Binding the port and showing the port used
            sock.bind((self.__host, self.__port))
            print(f"Binding the port {self.__port}")

            # Waiting for client to connect to server
            # Once listening, the client has to be connected before any options can be allowed
            sock.listen()

            return sock

        except socket.error as msg:
            print(f"Socket Initialization failed: {str(msg)}")

            return None

    def allow_conns(self, sock, extra_func = None):
        """ Start accepting connection from possible clients.\n
            The IP and Port are stored into a list, connections are arranged into a list as well\n\n
            Each client gets their own thread, """
        db_conn = db.create_connection(database)

        while not self.__kill:
            # Test message to indicate still listening for client(s)
            print(f"Listening....")

            # Accepting connection
            # First variable is the connection to conn and 2nd one is address of conn
            try:
                conn, addr = sock.accept()
                conn_List.append(conn)
                addr_List.append(addr)
                self.numOfConn = self.numOfConn + 1
                print(self.numOfConn)
            except socket.error as msg:
                print(f"Error while accepting socket: {str(msg)}")
            
            time = str(datetime.now().strftime("%H:%M:%S"))
            
            ## TRIGGER MSG
            label = "ROBO 00" + str(self.numOfConn)
            trigger = "Client " + label + " : Current time is " + time + "\n" + welcomeResp

            client_id = db.create_client(db_conn, (label,addr[0],addr[1],time,"-"))
            db.create_comms_archive(db_conn, (client_id,trigger, "-",str(datetime.now().strftime("%H:%M:%S"))))

            # Display connection message
            print(f"Connection Established with | {addr[0]}:{addr[1]} |")
            self.__thread.assign(target=self.__start_comms, args=(conn, client_id))
            self.__thread.start()

            
            conn.send(trigger.encode("utf-8"))
        
        sock.close()

    def __start_comms(self, conn, client_id):
        global timeout

        db_conn = db.create_connection(database)

        while not self.__kill:

            index = conn_List.index(conn)

            # Received from conn
            # Something sent through server-conn connection
            data = conn.recv(1024)
            db.create_comms_archive(db_conn, (client_id,"-", data.decode('utf-8'),str(datetime.now().strftime("%H:%M:%S"))))

            if not data:
                print("No command received")
                break
            
            # Exit function for conn
            if data.decode('utf-8').lower() in ["exit", "quit"]:
                print(f"Connection Closed with | {addr_List[index][0]}:{addr_List[index][1]} |")
                send = "Connection Closed with Divoc"
                conn.send(send.encode('utf-8'))
                db.create_comms_archive(db_conn, (client_id,send, "-",str(datetime.now().strftime("%H:%M:%S"))))
                db.update_client(db_conn, (str(datetime.now().strftime("%H:%M:%S")), client_id))
                conn.close()
                break
            elif data.decode('utf-8') == "@Quit":
                conn.send("Killing server".encode('utf-8'))
                conn.close()
                self.__kill = True
                break
            
            # Deploy functionality!
            # Comment  next 2 lines for server only debugging - FUNCTIONLESS STATE
            function = server_func(conn, data, db_conn)
            function.select(client_id)

    def kill(self, sock):
        self.__kill = True
        sock.close()
        print(f"Killed server....")