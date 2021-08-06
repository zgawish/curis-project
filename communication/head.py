import socket
import threading
import os
import time
from server import InstanceServer
from client import InstanceClient

class HeadServer(InstanceServer):
    children = {} # list() but can be any data structure like dict()
    PORT = 5060
    
    def __init__(self, port=PORT):
        self.ADDR = (self.SERVER, port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.set_up_clients()
        self.server_thread = threading.Thread(target=self.start_server)


    def set_up_clients(self):
        with open("children.txt", "r") as file:
            ips = file.read_lines()
            count = 0 # just to read first line for now
            for ip in ips:
                if count == 1:
                    break
                child = InstanceClient(5050, ip)
                self.children[ip] = child
                count += 1

    def start_server(self):
        self.server.listen()
        print("[LISTENING] Server is listening on " + self.SERVER)
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()

    def send_to_child(self, ip, msg):
        if ip in self.children:
            client = self.children[ip]
            r_msg = client.send_rcv(msg)
            return r_msg
        else:
            raise ValueError('ip is not in children!')


    def start(self):
        self.server_thread.start()




