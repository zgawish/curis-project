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
    if msg == "Message recieved":
        return True
    else:
        return False


def stop_instance(name):
    if is_ok(msg):
        request = service.instances().stop(project=project, zone=zone, instance=name)
        response = request.execute()
        return response
    else:
        return None


def main():
    msg = sys.argv[1]
    name = sys.argv[2]
    stop_instance(name)


if __name__ == "__main__":
    main()