/*
 * On the head node (within nextflow) start 3 processes (e.g.) and do the foll within each:
 * 1) Start an instance
 * 2) Start the corresponding clients and servers
 * 3) Send a command to every child node
 * 4) An output with the exit code is returned
 * 5) If the command was successful (exit code == 0), terminate the connections and then terminate the child node (instance)
 * 6) Once all the child nodes are terminated, the stage completes
*/

VMS = Channel.from('gridengine-on-gce-compute001', 'gridengine-on-gce-compute002', 'gridengine-on-gce-compute003')
path = "~/curis-project/"
// process that start instance from list and outputs client or server
process startInstances {
    input:
    val vm from VMS

    output:
    stdout ip into ips
    val vm into vms

    script:
    """
    python3 ${path}start_instance.py $vm
    """
    // local: python3 ~/Stanford/CURIS/curis-project/start_instance.py $vm

}

// result.view { it.trim() }


process sendMessage {
    input:
    val ip from ips
    val vm from vms

    output:
    // val r_msg into r_msgs
    stdout msg into msgs
    val vm into close_vms 

    script:
    """
    python3 ${path}send_msg.py $ip
    """
}

process closeInstances {
    input:
    val msg from msgs
    val vm from close_vms

    output:
    stdout result

    script:
    """
    python3 ${path}stop_instance.py $msg $vm
    """
}

result.view { it.trim() }