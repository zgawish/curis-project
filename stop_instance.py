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
    if msg == "0":
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
    ls = cmd.split(',')
    msg = ls[0].strip()
    name = ls[1].strip()
    # msg = sys.argv[1]
    result = msg.split('\n')
    code = result[-1]
    # name = sys.argv[2]
    print(stop_instance(name, code))


if __name__ == "__main__":
    main()