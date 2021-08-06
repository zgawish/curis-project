import os
path = "~/curis-project"
stream = os.popen("{path}./nextflow run {path}client.nf".format(path=path))
output = stream.read()
print(str(output))

