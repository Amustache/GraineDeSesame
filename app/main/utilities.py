import os
from random import choices
from string import Template

import bcrypt
import hashlib

import paramiko
from paramiko import SSHException
from paramiko.buffered_pipe import PipeTimeout

COMMAND_SRUN = "srun -c 8 --mem 32G --partition gpu-l40 --reservation=password_day_test --gres gpu:2 --time 120 bash -c '{command}'"
COMMAND_SQUEUE = "squeue -p gpu-l40 -u hhueber -h"


def hash_password(password: str) -> (str, bytes):
    password_encoded = password.encode("utf-8")
    salt = bcrypt.gensalt(10)
    bcrypt_hash = bcrypt.hashpw(password_encoded, salt)
    md5_hash = hashlib.md5(password_encoded).hexdigest()

    return md5_hash, bcrypt_hash


def check_hash(password: str, md5_hash: str, bcrypt_hash: bytes) -> (bool, bool):
    password_encoded = password.encode("utf-8")
    return md5_hash == hashlib.md5(password_encoded).hexdigest(), bcrypt.checkpw(password_encoded, bcrypt_hash)


def ssh_send_command(
        command: str,
        host: str,
        username: str,
        keyfilename: str = None,
        password: str = None,
        timeout: int = 5,
        **kwargs
):
    client = ssh_connect_client(host, keyfilename, password, username)

    try:
        ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(command, timeout=timeout)
    except SSHException as e:  # Most likely timeout
        return None

    return {
        "stdin": ssh_stdin,
        "stdout": ssh_stdout,
        "stderr": ssh_stderr,
    }


def ssh_send_script(
        script: str,
        host: str,
        username: str,
        keyfilename: str = None,
        password: str = None,
        timeout: int = 5,
        **kwargs
):
    client = ssh_connect_client(host, keyfilename, password, username)

    channel = client.invoke_shell()
    stdin = channel.makefile('wb')
    stdout = channel.makefile('rb')

    with open(script, "r") as f:
        template = Template(f.read())
        result = template.safe_substitute(**kwargs)
        print(result)
        stdin.write(result)

    res = stdout.read()

    stdout.close()
    stdin.close()
    client.close()

    return res


def ssh_connect_client(host, keyfilename, password, username):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.load_host_keys(os.path.expanduser("~/.ssh/known_hosts"))
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if keyfilename:
        k = paramiko.RSAKey.from_private_key_file(keyfilename)
        client.connect(hostname=host, username=username, pkey=k)
    elif password:
        client.connect(hostname=host, username=username, password=password)
    else:
        client.connect(hostname=host, username=username)

    return client


if __name__ == "__main__":
    md5_hash, bcrypt_hash = hash_password("TEST")
    md5_hash_password, _ = hash_password("password")  # Sanity chekc
    md5_hash_123456, _ = hash_password("123456")  # Sanity chekc
    print(md5_hash, bcrypt_hash)

    # Check False
    print(check_hash("test", md5_hash, bcrypt_hash))

    # Check True
    print(check_hash("TEST", md5_hash, bcrypt_hash))

    command = f"cd /users/hhueber/hashcat_test/hashcat-6.2.6 ; rm current_hash ; for var in \"{' '.join([md5_hash, md5_hash_password, md5_hash_123456])}\" ; do echo $var >> current_hash ; done ; module load cuda hashcat ; hashcat -m 0 -a 3 current_hash"

    # ssh_send_script("/home/hhueber/projects/GraineDeSesame/scripts/cluster_hashcat_simple.sh", "curnagl.dcsr.unil.ch", "hhueber", hashes=md5_hash)

    print(COMMAND_SRUN.format(command=command))
    # test = ssh_send_command("ls", "curnagl.dcsr.unil.ch", "hhueber")
    test = ssh_send_command(COMMAND_SRUN.format(command=command), "curnagl.dcsr.unil.ch", "hhueber")
    try:
        print(test["stdout"].read())
        print(test["stderr"].read())
    except TimeoutError:
        pass

    test = ssh_send_command(COMMAND_SQUEUE, "curnagl.dcsr.unil.ch", "hhueber")
    try:
        print(test["stdout"].read())
        print(test["stderr"].read())
    except TimeoutError:
        pass


def random_books() -> str:
    """
    tbh it's just so that there is a probability of having 🤓 somewhere.

    :return: Three emojis for a title.
    """
    BOOKS = {
        "📔": 0.6,
        "📕": 1.0,
        "📖": 0.5,
        "📗": 1.0,
        "📘": 1.0,
        "📙": 1.0,
        "📚": 0.3,
        "📓": 0.4,
        "📒": 0.7,
        "🤓": 0.1,
    }

    return ''.join(choices(population=list(BOOKS.keys()), weights=list(BOOKS.values()), k=3))
