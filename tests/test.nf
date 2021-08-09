#!/usr/bin/env nextflow

process sayHello {
    """
    echo 'Hello world!' > ~/curis-project/test.txt
    """
}