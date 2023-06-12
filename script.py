import subprocess

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if process.returncode != 0:
        raise Exception("Command failed: " + str(error))
    return output.decode('utf-8')

def container_exists(name):
    output = run_command("docker ps -q -f name={}".format(name))
    return len(output) > 0

def container_status(name):
    output = run_command("docker ps -aq -f status=exited -f name={}".format(name))
    return 'exited' if len(output) > 0 else None

def container_paused(name):
    output = run_command("docker ps -aq -f status=paused -f name={}".format(name))
    return 'paused' if len(output) > 0 else None

container_name = 'mycontainer'
image_tag = 'myapp-image:tag'

if container_exists(container_name):
    print("Container is working fine")
elif container_status(container_name) == 'exited':
    print("Container is paused. Restarting it...")
    run_command("docker start {}".format(container_name))
elif container_paused(container_name) == 'paused':
    print("Container is paused. Restarting it...")
    run_command("docker unpause {}".format(container_name))
else:
    print("Container doesn't exist, Creating it...")
    run_command("docker run -d --name {} {}".format(container_name, image_tag))
