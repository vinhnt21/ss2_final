import subprocess

# Run pip freeze command
result = subprocess.run(['pip', 'freeze'], stdout=subprocess.PIPE)

# Decode the output and write it to a file
with open('requirements.txt', 'w') as f:
    f.write(result.stdout.decode('utf-8'))