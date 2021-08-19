// error retry file

process retry { 
    errorStrategy { task.exitStatus == 0 ? 'terminate' : 'retry' }

    output:
    stdout result

    script:
    """
    python3 ~/Stanford/CURIS/curis-project/retry_test.py $task.attempt
    """
}

result.view { it.trim() }
