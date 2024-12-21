from datetime import datetime
import ftplib
from os import getenv
from dotenv import load_dotenv


class FtpTransfer ():
    def __init__(self, hostname: str = "", port: int = 0,  username: str = "", password: str = "") -> None:
        load_dotenv()
        if hostname != "":
            self.hostname = hostname
        else:
            self.hostname = getenv("FTP_HOSTNAME")
        if port != 0:
            self.port = port
        else:
            self.port = int(getenv("FTP_PORT"))
        if username != "":
            self.username = username
        else:
            self.username = getenv("FTP_USERNAME")
        if password != "":
            self.password = password
        else:
            self.password = getenv("FTP_PASSWORD")

    def transfer_csv(self, local_file: str):
        session = ftplib.FTP()
        date = datetime.now()

        remote_file = "{}_{}".format(date.strftime("%H%M"), local_file)
        session.connect(host=self.hostname, port=self.port)
        session.login(user=self.username, passwd=self.password)
        folderName = date.strftime("%Y%m%d").replace("/", "")
        if not folderName in session.nlst():
            session.mkd(folderName)
        session.cwd(folderName)
        with open(local_file, 'rb') as fp:
            session.storbinary("STOR %s" % remote_file, fp)
        session.quit()


# if __name__ == "__main__":
#     ftp = FtpTransfer(hostname="localhost", port=21,
#                            username="user", password="ftpasasa1221")
#     ftp.transfer_csv(local_file="dataset_test.csv")
