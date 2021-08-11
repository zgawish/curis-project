#!/usr/bin/env nextflow



def ipMap = [:]

vms = Channel.from('gridengine-on-gce-compute001', 'gridengine-on-gce-compute002', 'gridengine-on-gce-compute003')

// process that start instance from list and outputs client or server
process startInstances {
    input:
    val vm from vms

    output:
    stdout ip into ips
    val vm into vm_s

    """
    python3 ~/Stanford/CURIS/curis-project/start_instance.py $vm
    """
    // local: python3 ~/Stanford/CURIS/curis-project/start_instance.py $vm
    // gce: ~/curis-project/start_instance.py $vm
}

process check {
    input:
    val ip from ips
    val vm from vm_s

    output:
    stdout result
    """
    echo "$vm: $ip"
    """

}

result.view { it.trim() }
