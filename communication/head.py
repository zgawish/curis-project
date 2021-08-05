from server import InstanceServer
from client import InstanceClient

class HeadServer(InstanceServer):
    children = [] # list() but can be any data structure like dict()

    def __init__(self, port=self.PORT):
        self.ADDR = (self.SERVER, port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.set_up_clients()

    def set_up_clients(self):
        with open("children.txt", "r") as file:
            ips = file.read_lines()
            count = 0 # just to read first line for now
            for ip in ips:
                if count == 1:
                    break
                child = InstanceClient(5050, ip)
                count += 1

