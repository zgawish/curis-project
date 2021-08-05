from server import InstanceServer
from client import InstanceClient

class HeadServer(InstanceServer):
    children = []

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.set_up_clients()

    def set_up_clients(self):
        with open("children.txt", "r") as file:
            lines = file.read_lines()
            count = 0 # just to read first line for now
            for line in lines:
                

