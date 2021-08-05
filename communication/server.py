import socket
import threading
import os
import time

class InstanceServer:
    HEADER = 1024
    PORT = 5060
    SERVER = socket.gethostbyname(socket.gethostname()) # 192.168.86.23
    ADDR = None
    FORMAT = 'utf-8'
    DISCONNECT_MSG = "!DISCONNECT"
    REQUEST_MSG = "!REQUEST"

    def __init__(self, port=self.PORT):
        self.ADDR = (self.SERVER, port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)


    def recieve(self, conn):
        msg_length = conn.recv(self.HEADER).decode(self.FORMAT) # recieve size of message then actual string
        if msg_length: # if theres a msg
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(self.FORMAT)
            return msg
        return ""


    def send(self, conn, msg):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        conn.send(send_length)
        conn.send(message)


    def run_command(self, args):
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


    def parse_message(self, msg):
        args = msg.split()
        if args[0] == 'cmd': # command constant
            return self.run_command(args)
        else:
            return "Message recieved"


    def handle_client(self, conn, addr):
        print("[NEW CONNECTION] " + str(addr[0]) + " connected.")
        print("[ACTIVE CONNECTIONS] " + str(threading.activeCount() - 1))
        connected = True
        while connected:
            msg = self.recieve(conn)
            if msg == self.DISCONNECT_MSG:
                connected = False
                self.send(conn, self.DISCONNECT_MSG)
            if msg != "": 
                print(str(addr[0]) + ": " + msg)
                send_msg = self.parse_message(msg)
                print(send_msg)
                self.send(conn, send_msg)
        conn.close()


    def start_server(self):
        self.server.listen()
        print("[LISTENING] Server is listening on " + self.SERVER)
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()


def main():
    server = InstanceServer()
    server.start_server()

if __name__ == "__main__":
    main()
