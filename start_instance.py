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


def start_instance(name):
    request = service.instances().start(project=project, zone=zone, instance=name)
    response = request.execute()
    return response


def get_ip(name):
    request = service.instances().get(project=project, zone=zone, instance=name)
    response = request.execute()
    return response['networkInterfaces'][0]['networkIP']


def main():
    name = sys.argv[1]
    start_instance(name)
    print(get_ip(name))


if __name__ == "__main__":
    main()