/*
 * On the head node (within nextflow) start 3 processes (e.g.) and do the foll within each:
 * 1) Start an instance
 * 2) Start the corresponding clients and servers
 * 3) Send a command to every child node
 * 4) An output with the exit code is returned
 * 5) If the command was successful (exit code == 0), terminate the connections and then terminate the child node (instance)
 * 6) Once all the child nodes are terminated, the stage completes
*/

vms = Channel.from('gridengine-on-gce-compute001', 'gridengine-on-gce-compute002', 'gridengine-on-gce-compute003')

// process that start instance from list and outputs client or server
process startInstances {
    input:
    val vm from vms

    output:
    val ip into ips

    script:
    """
    python3 ~/Stanford/CURIS/curis-project/start_instance.py $vm
    """
}

// result.view { it.trim() }


process sendMessage {
    input:
    val ip from ips

    output:
    // val r_msg into r_msgs
    stdout result
    """
    #!/usr/bin/python3

    from communication.client import InstanceClient

    client = InstanceClient(5060, $ip)
    client.connect_client()
    r_msg = client.quick_send("Dear $ip: Hello from 10.128.0.3!")
    print("$ip: " + r_msg)
    """
}

result.view { it.trim() }






// process that taskes in client or server and either runs head or child using python

// return code and end instance

// Note:pickle object to save status?