#!/bin/bash -ue
sleep 5
gcloud compute ssh --zone "us-central1-a" "gridengine-on-gce-compute001"  --project "spry-notch-318823" -- 'cd ~/curis-project/ && ./nextflow run client.nf'
