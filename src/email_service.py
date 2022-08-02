"""
Module is responsible for donwload send operation
from the gmail account.
"""

import logging
import logging.config
import sys
from datetime import datetime
from email import message_from_bytes
from imaplib import IMAP4_SSL
from os import path

sys.dont_write_bytecode = True

logging.config.fileConfig("src/logging.conf")
# pylint:disable=unused-private-member,unnecessary-pass
class EmailService:
    """class doc string"""

    def __init__(self, username: str, password: str, imap: str) -> None:
        self._username = username
        self._password = password
        self._imap = imap
        self._connection = IMAP4_SSL(self._imap)
        logging.info(" %s class is initialised.", EmailService.__name__)

    def __get_email_id(self):
        """function doc string"""
        result = None
        try:
            self._connection.login(self._username, self._password)
            self._connection.select("INBOX")
            logging.info(" Connection successful, searching email.")
            response, email_id = self._connection.search(None, "SUBJECT", "Records")
            if response == "OK":
                fetch_res, data = self._connection.fetch(email_id[0], "(RFC822)")
                if fetch_res:
                    logging.info(" Email fetched successfully.")
                    result = data
        except Exception as get_id_err:
            logging.error(" Error in %s %s", self.__get_email_id.__name__, get_id_err)
            raise get_id_err
        return result

    def __save_attachment(self, byte_message):
        """doc string"""
        try:
            file_name = "Record_" + datetime.now().strftime("%Y_%m_%d") + ".csv"
            logging.info(" Converting bytes data to normal string.")
            raw_message = message_from_bytes(byte_message)
            for part in raw_message.walk():
                if bool(part.get_filename()):
                    file_path = path.join("src/", file_name)
                    logging.info(" Saving donwload file at %s", file_path)
                    with open(file_path, "wb") as file:
                        file.write(part.get_payload(decode=True))
            logging.info(" Saved file successfully")
        except Exception as save_att_err:
            logging.error(" Error in %s %s", self.__save_attachment.__name__, save_att_err)
            raise save_att_err

    def _create_message(self):
        """doc string"""
        pass

    def __send_message(self):
        """doc string"""
        pass

    def start(self):
        """doc stirng"""
        try:
            logging.info(" Process started.")
            data = self.__get_email_id()
            self.__save_attachment(data[0][1])
            logging.info(" Process completed. ")
        except Exception as start_err:
            logging.error(" Error in %s %s", self.start.__name__, start_err)
            raise start_err


if __name__ == "__main__":
    email = EmailService("anoopprsingh@gmail.com", "tncjcbhpbrscxswu", "imap.gmail.com")
    email.start()
