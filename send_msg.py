import sys
from communication.client import InstanceClient

def send_msg(ip, msg): # 2
    client = InstanceClient(5060, ip)
    client.connect_client()
    # r_msg = client.quick_send("Dear {}: Hello from 10.128.0.3!".format(ip)) # 1
    r_msg = client.quick_send(msg) # 2
    return r_msg

def main():
    ip = sys.argv[1]
    msg = sys.argv[2] # 2
    r_msg = send_msg(ip, msg) # 2
    print(r_msg) # 1
    results = r_msg.split('\n')
    exit(int(results[-1])) # exits with status
    



if __name__ == "__main__":
    main()