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
// path = "~/curis-project/"
path = "~/Stanford/CURIS/curis-project/"
cmd = "curl ifconfig"
cmd = "ls"
// process that start instance from list and outputs client or server
process startInstances {
    input:
    val vm from VMS

    output:
    val vm into vms

    script:
    """
    python3 ${path}start_instance.py $vm
    """
}

process closeInstances {
    input:
    val vm from vms

    output:
    stdout result

    script:
    """
    python3 ${path}stop_instance.py "a\n0" $vm
    """
}



// r_msgs.view { "Status of sending msg: $it"}
// msgs.view { "Return value of sending cmd"}
result.view { it.trim() }