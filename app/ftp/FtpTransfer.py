import os
import paramiko
from datetime import datetime


class FtpTransfer ():
    def __init__(self, hostname, username, password) -> None:
        self.hostname = hostname
        self.username = username
        self.password = password

    def transfer_csv(self, local_file: str):
        self.sftp = self.ssh.open_sftp()
        remote_file = local_file.replace(".csv", "{}.csv".format(datetime.now("%y%j%H%M")))
        self.sftp.put(localpath=local_file, remotepath=remote_file)

    def connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.hostname, username=self.username,
                         password=self.password)

    def close(self):
        self.sftp.close()
        self.ssh.close()
