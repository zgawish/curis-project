import sys
from pprint import pprint

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

credentials = GoogleCredentials.get_application_default()
service = discovery.build('compute', 'v1', credentials=credentials)
# Project ID for this request.
project = 'spry-notch-318823'
# The name of the zone for this request.
zone = 'us-central1-a'


def is_ok(msg):
    if msg == "recieved":
        return True
    else:
        return False


def stop_instance(name, msg):
    if is_ok(msg):
        request = service.instances().stop(project=project, zone=zone, instance=name)
        response = request.execute()
        return "{} is stopped".format(name)
    else:
        return None


def main():
    cmd = sys.argv[1]
    ls = cmd.split(', \n')
    msg = ls[0]
    name = ls[1]
    print(ls)
    # print(stop_instance(name, msg))


if __name__ == "__main__":
    main()