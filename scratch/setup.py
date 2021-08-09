import os, sys
from pprint import pprint

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

credentials = GoogleCredentials.get_application_default()

service = discovery.build('compute', 'v1', credentials=credentials)

# Project ID for this request.
project = 'spry-notch-318823'

# The name of the zone for this request.
zone = 'us-central1-a'

head = 'elasticluster-test-instance'

instances = []
def start_instances():
    try:
        request = service.instances().list(project=project, zone=zone)
        while request is not None:
            response = request.execute()

            for instance in response['items']:
                #pprint(instance['name'])
                instances.append(instance['name'])
                request2 = service.instances().start(project=project, zone=zone, instance=instance['name'])
                response2 = request2.execute()
                #pprint(response2)



            request = service.instances().list_next(previous_request=request, previous_response=response)
            return True
    except Exception:
        return False

"""
gcloud compute ssh --zone "us-central1-a" "<name>"  --project "spry-notch-318823" -- '~/curis-project/communication/ && python3 client.py'
"""

def set_up_server():
    cmd = "gcloud compute ssh --zone 'us-central1-a' 'elasticluster-test-instance'  --project 'spry-notch-318823' -- 'cd ~/curis-project/communication/ && python3 serverclass.py'"
    stream = os.popen(cmd)
    output = stream.read()
    print(str(output))


def set_up_client(name):
    if name == 'gridengine-on-gce-compute001': # just for now because repos are not installed
        cmd = "gcloud compute ssh --zone 'us-central1-a' '"  + name + "'  --project 'spry-notch-318823' -- 'cd ~/curis-project/communication/ && python3 client.py'"
        stream = os.system(cmd)

def set_up_clients():
    request = service.instances().list(project=project, zone=zone)
    while request is not None:
        response = request.execute()

        for instance in response['items']:
            if instance != 'elasticluster-test-instance':
                set_up_client(instance['name'])


        request = service.instances().list_next(previous_request=request, previous_response=response)

def main():
#    start_instances()
#    set_up_server()
#    set_up_clients()
    print("ALL DONE")

    
if __name__ == "__main__":
    main()

