import subprocess
import json

command = 'php derive -g --mnemonic="dinosaur ring proud exclude hospital hair december slush garbage ensure noble toward" --cols=path,address,privkey,pubkey --format=json'

p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
(output,err) = p.communicate()
p.status=p.wait()

# print(output)

keys=json.loads(output)
# print(keys)

print(keys[0]['address'])
