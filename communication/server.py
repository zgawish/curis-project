import socket
import threading
import os
import time
import sys

class InstanceServer:
    HEADER = 1024
    PORT = 5060
    SERVER = socket.gethostbyname(socket.gethostname()) # 192.168.86.23
    ADDR = None
    FORMAT = 'utf-8'
    DISCONNECT_MSG = "!DISCONNECT"
    REQUEST_MSG = "!REQUEST"

    def __init__(self, port=PORT):
        self.ADDR = (self.SERVER, port)
        self.port = port
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


    def run_command(self, args, addr):
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
            from_who = str(addr[0]) + ": "
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            os.system("echo '{}: {} \n {}' >> /home/ziygawish/curis-project/cmds".format(current_time, command, str(output)))
            # return str(output)
            return "recieved"


    def parse_message(self, msg, addr):
        args = msg.split()
        if args[0] == 'cmd': # command constant
            return self.run_command(args, addr)
        else:
            return "recieved"


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
                from_who = str(addr[0]) + ": " + msg
                print(from_who)
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)
                os.system("echo '{}: {}' >> /home/ziygawish/curis-project/msg".format(current_time, from_who))
                send_msg = self.parse_message(msg, addr)
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


    def __repr__(self):
        return "InstanceServer({}, {})".format(self.SERVER, self.port)


    def __str__(self):
        txt = "Server on (IP: {}, PORT: {})"
        return txt.format(self.SERVER, self.port)


def main():
    port = sys.argv[1]
    server = InstanceServer(int(port))
    server.start_server()

if __name__ == "__main__":
    main()