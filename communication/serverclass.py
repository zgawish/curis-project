import socket
import threading
import os
import time

class SocketServer:
    HEADER = 1024
    PORT = 5050
    SERVER = socket.gethostbyname(socket.gethostname()) # 192.168.86.23
    ADDR = (SERVER, PORT)
    FORMAT = 'utf-8'
    DISCONNECT_MSG = "!DISCONNECT"
    REQUEST_MSG = "!REQUEST"
    RECENT = {}

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)

        self.new_data = False # indicator of new data
        self.num_conns = 0  # number of connections

    def parse_message(self, msg):
        args = msg.split()
        if args[0] == 'cmd': # command constant
            if len(args) == 1:
                return "Error: Send arguments with cmd"
            else:
                command = ""
                for arg in args[1:len(args) - 1]:
                    command += arg
                    command += " "
                command += args[-1]
                stream = os.popen(command)
                output = stream.read()
                return str(output)
        else:
            return "Message recieved"


    def handle_client(self, conn, addr):
        print("[NEW CONNECTIONS] " + str(addr[0]) + " connected.")

        connected = True
        while connected:
            msg_length = conn.recv(self.HEADER).decode(self.FORMAT) # recieve size of message then actual string
            if msg_length: # if theres a msg
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(self.FORMAT)
                if msg == self.DISCONNECT_MSG:
                    connected = False
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    conn.send(("DISCONNECTED: " + current_time).encode(self.FORMAT))
                elif msg == self.REQUEST_MSG:
                    conn.send(("SENDING WORK OVER").encode(self.FORMAT))
                else:    
                    print(str(addr[0]) + ": " + msg)
                    send_msg = self.parse_message(msg)
                    print(send_msg)
                    conn.send(send_msg.encode(self.FORMAT))
        conn.close()
        self.num_conns -= 1
        print("[ACTIVE CONNECTIONS] " + str(self.num_conns))


    def start_server(self):
        self.server.listen()
        print("[LISTENING] Server is listening on " + self.SERVER)
        while True:
            conn, addr = self.server.accept()
            self.num_conns += 1
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print("[ACTIVE CONNECTIONS] " + str(threading.activeCount() - 1))


def main():
    server = SocketServer()
    server.start_server()

if __name__ == "__main__":
    main()
