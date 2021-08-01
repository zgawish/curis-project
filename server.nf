

process setup {
    """
    python3 ~/curis-project/setup.py
    """
}

process startServer {
    """
    python3 ~/curis-project/communication/serverclass.py &
    """
}

process sendCommands {
    """
    gcloud compute ssh --zone "us-central1-a" "gridengine-on-gce-compute001"  --project "spry-notch-318823" -- 'cd ~/curis-project/ && ./nextflow run client.nf'
    """
}