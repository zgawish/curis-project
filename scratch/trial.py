from pprint import pprint

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

credentials = GoogleCredentials.get_application_default()

service = discovery.build('compute', 'v1', credentials=credentials)

# Project ID for this request.
project = 'spry-notch-318823'  # TODO: Update placeholder value.

# The name of the zone for this request.
zone = 'us-central1-a'  # TODO: Update placeholder value.

# Name of the instance resource to start.
instance = 'elasticluster-test-instance'  # TODO: Update placeholder value.

request = service.instances().start(project=project, zone=zone, instance=instance)
response = request.execute()

# TODO: Change code below to process the `response` dict:
# pprint(response)

request = service.projects().get(project=project)
response = request.execute()

# TODO: Change code below to process the `response` dict:
#pprint(response)

# get list
request = service.instances().list(project=project, zone=zone)
while request is not None:
    response = request.execute()

    for instance in response['items']:
        # TODO: Change code below to process each `instance` resource:
        pprint(instance['name'])
        request2 = service.instances().start(project=project, zone=zone, instance=instance['name'])
        response2 = request2.execute()
        pprint(response2)
        request3 = service.instances().stop(project=project, zone=zone, instance=instance['name'])
        response3 = request3.execute()
        pprint(response3)


    request = service.instances().list_next(previous_request=request, previous_response=response)