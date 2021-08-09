/*
 * On the head node (within nextflow) start 3 processes (e.g.) and do the foll within each:
 * 1) Start an instance
 * 2) Start the corresponding clients and servers
 * 3) Send a command to every child node
 * 4) An output with the exit code is returned
 * 5) If the command was successful (exit code == 0), terminate the connections and then terminate the child node (instance)
 * 6) Once all the child nodes are terminated, the stage completes
*/

// process thaty start instance from list and outputs client or server

// process that taskes in client or server and either runs head or child using python

// return code and end instance

// Note:pickle object to save status?