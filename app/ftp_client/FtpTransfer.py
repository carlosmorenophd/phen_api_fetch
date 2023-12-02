from datetime import datetime
import ftplib
import os

class FtpTransfer ():
    def __init__(self, hostname: str, port: int,  username: str, password: str) -> None:
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port

    def transfer_csv(self, local_file: str):
        session = ftplib.FTP()
        date = datetime.now()


        remote_file = local_file.replace(
            ".csv", "_{}.csv".format(date.strftime("%H%M")))
        session.connect(host=self.hostname, port=self.port)
        session.login(user=self.username, passwd=self.password)
        folderName = date.strftime("%Y%m%d").replace("/","")
        if not folderName in session.nlst():
            session.mkd(folderName)
        session.cwd(folderName)
        with open(local_file, 'rb') as fp:
            session.storbinary("STOR %s"%remote_file, fp)
        session.quit()


# if __name__ == "__main__":
#     ftp = FtpTransfer(hostname="localhost", port=21,
#                            username="user", password="ftpasasa1221")
#     ftp.transfer_csv(local_file="dataset_test.csv")
