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
// path = "~/Stanford/CURIS/curis-project/"
cmd = "curl ifconfig"
// cmd = "ls"
// cmd = "python3 /home/ziygawish/curis-project/random_num.py"
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
}


process sendMessage {
    maxRetries = { task.exitStatus == 0 ? 0 : 3 }

    input:
    val ip from ips
    val vm from vms

    output:
    stdout r_msg into r_msgs
    val vm into next_vm
    val ip into ips_cmds

    script:
    //     python3 ${path}send_msg.py $ip hello!
    send_msg =  " python3 ${path}send_msg.py $ip hello! "
    """
    ${send_msg}
    """
}

// r_msgs.view { "Status of sending msg: $it"}

process sendCommand {
    maxRetries = { task.exitStatus == 0 ? 0 : 3 }

    input:
    val ip from ips_cmds
    val vm from next_vm

    output:
    val vm into close_vms
    stdout msg into msgs
    
    script:
    """
    python3 ${path}send_msg.py $ip '${cmd}'
    """
}

// msgs.view { "Return value of sending cmd"}

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