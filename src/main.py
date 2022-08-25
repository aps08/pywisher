"""
This is main module, which inherits and uses the other
two modules named as GetAttachMentService and SendEmailService.
"""

import logging
import logging.config
import os
import sys
from datetime import datetime
from io import StringIO
from typing import Tuple

import pandas as pd

from helper import GetAttachMentService, SendEmailService

sys.dont_write_bytecode = True
logging.config.fileConfig("logging.conf")


class Pywisher(GetAttachMentService, SendEmailService):
    """
    This class the other two clases for
    downloading and sending email.
    """

    def __init__(self, username: str, password: str):
        """Constructor"""
        self.__now = datetime.now()
        self.__delete_logger_weekly()
        logging.info(
            " %s class is initailised. Datetime %s", Pywisher.__name__, self.__now
        )
        GetAttachMentService.__init__(self, username, password)
        SendEmailService.__init__(self, username, password)
        
    def __delete_logger_weekly(self) -> None:
        """
        Deletes the log file on every sunday.
        """
        try:
            log_file = "pywisher.log"
            today = self.__now.strftime("%A")
            if today == "Saturday" and os.path.exists(log_file):
                os.remove(log_file)
                logging.config.fileConfig("logging.conf")
        except Exception as del_err:
            raise del_err

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
        data_frame = None
        try:
            file_content = StringIO(self.save(key))
            logging.info(" Creating pandas dataframe using the file content recieved.")
            data_frame = pd.read_csv(file_content, sep=",", index_col="id")
        except Exception as down_read_err:
            logging.error(" Error in %s\n%s", self.__download_and_read.__name__, down_read_err)
            raise down_read_err
        return data_frame

    def __process_file(self, data: pd.DataFrame) -> None:
        """
        Process the data, and check if anyone is having brithday today.
        If yes, sends them a birthday wish.

        argument:
            data: pandas dataframe
        """
        try:
            day = datetime.now().day
            month = datetime.now().month
            data["dob"] = pd.to_datetime(data["dob"], format="%d-%m-%Y")
            logging.info(" Creating new column named sendemail.")
            logging.info(" sendemail column is True if birthday is today.")
            for index, row in data.iterrows():
                if (day == row["dob"].dt.day.astype(int) and \
                    month == data["dob"].dt.month.astype(int)):
                    data["sendemail"] = True
                else:
                    data["sendemail"] = False
            itr_data = data.query("sendemail==True")
            nums = len(itr_data)
            print(data["sendemail"])
            if nums > 0:
                for index, row in itr_data.iterrows():
                    logging.info(" Sending email to ID %s", index)
                    print("yes")
#                     self.send(row["email"], "Happy Birthday " + row["firstname"])
            else:
                logging.info(" No birthday today.")
        except Exception as proc_err:
            raise proc_err

    def start(self, search_subject_key: str):
        """
        Function is responsible for triggering the whole process.

        argument:
            search_subject_key: key for searching email.
        """
        try:
            logging.info(" Triggering the whole process.")
            data = self.__download_and_read(search_subject_key)
            self.__process_file(data)
            logging.info(" Whole process completed successfully.")
        except Exception as start_err:
            logging.error(" Error in %s\n%s", self.start.__name__, start_err)
            raise start_err
        logging.shutdown()


if __name__ == "__main__":
    key_id = os.environ.get("KEY_ID")
    key_secret = os.environ.get("KEY_SECRET")
    search_key = os.environ.get("SEARCH_KEY")
    Pywisher = Pywisher(key_id, key_secret)
    Pywisher.start(search_key)
