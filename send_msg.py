import sys
from communication.client import InstanceClient

def send_msg(ip):
    client = InstanceClient(5060, ip)
    client.connect_client()
    r_msg = client.quick_send("Dear {}: Hello from 10.128.0.3!").format(ip)
    return ip + ": " + r_msg

def main():
    ip = sys.argv[1]
    print(send_msg(ip))


if __name__ == "__main__":
    main()