import socket
import threading
import os
import time
from server import InstanceServer
from client import InstanceClient

class ChildServer(InstanceServer):
    client = None # list() but can be any data structure like dict()
    PORT = 5060
    HEAD_PORT = 5070


    def __init__(self, port=PORT, head_server="10.128.0.3", head_port=HEAD_PORT):
        self.ADDR = (self.SERVER, port)
        self.port = port
        self.head_port = head_port
        self.head_server = head_server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.set_up_head()
        self.server_thread = threading.Thread(target=self.start_server)


    def set_up_head(self):
        child = InstanceClient(self.head_port, self.head_server)
        self.client = child


    def start_server(self):
        self.server.listen()
        print("[LISTENING] Server is listening on " + self.SERVER)
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()


    def send_to_head(self, msg):
        self.client.connect_client()
        r_msg = self.client.send_rcv(msg)
        self.client.disconnect()
        return r_msg


    def start(self):
        self.server_thread.start()


    def __repr__(self):
        return "HeadServer({}, {})".format(self.SERVER, self.port)


    def __str__(self):
        txt = "Server on (IP: {}, PORT: {}). Clients connected to PORT: {}"
        return txt.format(self.SERVER, self.port, self.CHILDREN_PORT)
