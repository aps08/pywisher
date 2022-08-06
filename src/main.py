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
from datetime import datetime
from typing import Tuple

import pandas as pd

from helper import GetAttachMentService, SendEmailService

sys.dont_write_bytecode = True
logging.config.fileConfig("src/logging.conf")


class Pywisher(GetAttachMentService, SendEmailService):
    """
    This class the other two clases for
    downloading and sending email.
    """

    def __init__(self, username: str, password: str):
        """Constructor"""
        GetAttachMentService.__init__(self, username, password)
        SendEmailService.__init__(self, username, password)
        file = "src/records.csv"
        if os.path.exists(file):
            os.remove(file)
        logging.info(" Pywisher class is initailised.")

    def __download_and_read(self, key: str) -> Tuple[str, pd.DataFrame]:
        """
        Function is responsible for triggering the GetAttachMentService
        class, and generating the csv file for processing.

        argument:
            key: a key for searching from inbox email.
        return:
            file_path: where is the file is generated.
            data_frame: pandas dataframe generated after
                        reading the donwloaded file.
        """
        file_path, data_frame = None, None
        try:
            file_path = self.save(key)
            logging.info(" Waiting 3 seconds for the file to be generated.")
            time.sleep(3)
            data_frame = pd.read_csv(file_path, sep=",", index_col="id")
        except Exception as down_read_err:
            logging.error(" Error in %s\n%s", self.__download_and_read.__name__, down_read_err)
            raise down_read_err
        logging.info(" Getting file path and data as a pandas dataframe.")
        return file_path, data_frame

    def __process_file(self, data: pd.DataFrame) -> None:
        """
        Process the data, and check if anyone is having brithday today.
        If yes, sends them a birthday wish.

        argument:
            data: pandas dataframe
        """
        try:
            self.__remove_file("src/records.csv")
            day = datetime.now().day
            month = datetime.now().month
            logging.info(" Creating new column named email.")
            data["dob"] = pd.to_datetime(data["dob"], format="%d-%m-%Y")
            condition = (day == data["dob"].dt.day.astype(int)) & (
                month == data["dob"].dt.month.astype(int)
            )
            data["sendemail"] = condition
            itr_data = data.query("sendemail==True")
            nums = len(itr_data)
            if nums > 0:
                logging.info(" Nedd to send email to %s people.", nums)
                for index, row in itr_data.iterrows():
                    logging.info(" Sending email to %s", index)
                    self.send(row["email"], "Happy Birthday " + row["firstname"])
                logging.info(" Sent the email to everyone having birthday today.")
            else:
                logging.info(" No birthday today.")
        except Exception as proc_err:
            raise proc_err

    def __remove_file(self, path: str) -> None:
        """
        Delete the csv file after operation is done.

        argument:
            path: where the file is present.
        """
        if os.path.exists(path):
            logging.info(" Removing the csv file, which was downloaded.")
            os.remove(path)

    def start(self, search_subject_key: str):
        """
        Function is responsible for triggering the whole process.

        argument:
            search_subject_key: key for searching email.
        """
        try:
            logging.info(" Triggering the whole process.")
            path, data = self.__download_and_read(search_subject_key)
            self.__process_file(data)
            self.__remove_file(path)
            logging.info(" Whole process completed successfully.")
        except Exception as start_err:
            logging.error(" Error in %s\n%s", self.start.__name__, start_err)
            raise start_err


if __name__ == "__main__":
    Pywisher = Pywisher("anoopprsingh@gmail.com", "tncjcbhpbrscxswu")
    Pywisher.start("qEjXyA3SVhN3FEn")
