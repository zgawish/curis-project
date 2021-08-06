import os

stream = os.popen("./nextflow run client.nf")
output = stream.read()
print(str(output))

