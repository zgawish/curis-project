import socket
import threading
import os
import time
from server import InstanceServer
from client import InstanceClient

class HeadServer(InstanceServer):
    children = {} # list() but can be any data structure like dict()
    PORT = 5050
    CHILDREN_PORT = 5060


    def __init__(self, port=PORT, children_port=CHILDREN_PORT):
        self.ADDR = (self.SERVER, port)
        self.port = port
        self.children_port = children_port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.set_up_clients()
        self.server_thread = threading.Thread(target=self.start_server)


    def set_up_clients(self):
        with open("children.txt", "r") as file:
            ips = file.read().splitlines()
            count = 0 # just to read first line for now
            for ip in ips:
                if count == 1:
                    break
                child = InstanceClient(self.children_port, ip)
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
            client.connect_client()
            r_msg = client.send_rcv(msg)
            client.disconnect()
            return r_msg
        else:
            raise ValueError('ip is not in children!')


    def start(self):
        self.server_thread.start()


    def __repr__(self):
        return "HeadServer({}, {})".format(self.SERVER, self.port)


    def __str__(self):
        txt = "Server on (IP: {}, PORT: {}). Clients connected to PORT: {}"
        return txt.format(self.SERVER, self.port, self.children_port)
