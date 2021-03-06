import socket
import time
import sys

PORT = 5050
SERVER = "10.128.0.3" ### IP OF SERVER ###
"""
InstanceClient
--------------
Class that sends and receives responses to a server  
"""
class InstanceClient:
    HEADER = 1024
    FORMAT = 'utf-8'
    DISCONNECT_MSG = "!DISCONNECT"
    REQUEST_MSG = "!REQUEST"
    COMPLETED_MSG = "!COMPLETED"


    def __init__(self, port, server):
        self.server = server
        self.port = port
        self.addr = (server, port)
        self.connected = False
        self.client = None

    def connect_client(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.addr)
        self.connected = True
        return self.connected


    # private
    def receive(self):
        msg_length = self.client.recv(self.HEADER).decode(self.FORMAT) # receive size of message then actual string
        if msg_length: # if theres a msg
            msg_length = int(msg_length)
            msg = self.client.recv(msg_length).decode(self.FORMAT)
            return msg
        return ""


    # commands start with a "cmd"
    def send(self, msg):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)


    # should be used for sending basic message
    def send_rcv(self, msg):
        self.send(msg)
        r_msg = self.receive()
        return r_msg

    
    # connects if not connected and disconnects after recieving a message
    def quick_send(self, msg):
        if not self.connected:
            self.connect_client()
        r_msg = self.send_rcv(msg)
        self.disconnect()
        return r_msg


    # disconnect 
    def disconnect(self):
        r_msg = self.send_rcv(self.DISCONNECT_MSG)
        if r_msg == self.DISCONNECT_MSG:
            self.client.close()
            self.connected = False
            return True
        return False


    def __repr__(self):
        return "InstanceClient({}, {})".format(self.server, self.port)


    def __str__(self):
        txt = "Client connected to (IP: {}, PORT: {})"
        return txt.format(self.server, self.port)