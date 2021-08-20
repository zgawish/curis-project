// error retry file
path = "~/curis-project/"

process retry { 
    errorStrategy { task.exitStatus == 0 ? 'terminate' : 'retry' }

    output:
    stdout result

    script:
    """
    python3 ${path}retry_test.py $task.attempt
    """
}

// local: ~/Stanford/CURIS/

result.view { it.trim() }
