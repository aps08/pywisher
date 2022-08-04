"""
save record - returns name
use the save to read the record
check if some one is having brithday today
if there is a birthday today.
delete records.csv if exist
"""
import logging
import logging.config
import os
import sys
import time

import pandas as pd

from helper.get_attachment import GetAttachMentService
from helper.send_email import SendEmailService

sys.dont_write_bytecode = True
logging.config.fileConfig("src/logging.conf")


class Pywisher(GetAttachMentService, SendEmailService):
    """def"""

    def __init__(self, username: str, password: str) -> None:
        GetAttachMentService.__init__(self, username, password)
        SendEmailService.__init__(self, username, password)
        file = "src/records.csv"
        if os.path.exists(file):
            os.remove(file)
        logging.info(" Pywisher class is function initailised.")

    def __download_and_read(self, key: str):
        """doc string"""
        file_path = self.save(key)
        data_frame = None
        retries = 10
        if not os.path.exists(file_path) and retries > 0:
            time.sleep(1)
            retries -= 1
        data_frame = pd.read_csv(file_path, sep=",", index_col="id")
        print(data_frame)

    def start(self, search: str):
        """doc string"""
        self.__download_and_read(search)


if __name__ == "__main__":
    Pywisher = Pywisher("email", "password")
    Pywisher.start("subjectkey")
