from paramiko import SSHClient, PasswordRequiredException
from scp import SCPClient
import os
import getpass


class pi_scp_send:

    def __init__(self, username, hostname, p = getpass.getpass(prompt='Enter your private key password, if none hit "ENTER"'), remote_dir='~/', port=22):
        self.username = username
        self.hostname = hostname
        #self.filename = filename
        self.remote_dir = remote_dir
        self.port = port
        self.p = p

    def trafficManager(self, fileList):
        if len(fileList) > 0:
            file = fileList.pop(1)
            return file


    def scpSender(self, filename):
        ssh = SSHClient()
        ##In terminal, run: ssh -o GlobalKnownHostsFile=/dev/null -o UserKnownHostsFile=./known_hosts pi@raspberrypi.local to create a separate known_hosts file
        ssh.load_host_keys(os.path.join(os.path.dirname(__file__), 'known_hosts'))
        if len(self.p) > 0:
            ssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.p)
        else:
            try:
                ssh.connect(hostname=self.hostname, port=self.port, username=self.username)
            except PasswordRequiredException:
                ssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.p)
        scp = SCPClient(ssh.get_transport())
        scp.put(filename, recursive=True, remote_path=self.remote_dir)
        scp.close()
        ssh.close()





