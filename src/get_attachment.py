"""
This module is responsible for downloading the
attachment from gmail, which contains the record.
"""

import logging
import logging.config
import sys
from email import message_from_bytes
from imaplib import IMAP4_SSL
from os import path

sys.dont_write_bytecode = True

logging.config.fileConfig("src/logging.conf")


class GetAttachMentService:
    """This class is responsible for downloading the attachment."""

    def __init__(self, username: str, password: str):
        """Constructor"""
        self._username = username
        self._password = password
        self._imap = "imap.gmail.com"
        self._connection = IMAP4_SSL(self._imap)
        logging.info(" %s class is initialised.", GetAttachMentService.__name__)

    def __get_email_in_bytes(self, search_key: str) -> list:
        """
        Gets email message in bytes, using message ID.

        return:
            result: email message in bytes.
        """
        result = None
        try:
            self._connection.login(self._username, self._password)
            self._connection.select("INBOX")
            logging.info(" Connection successful, searching email in inbox.")
            response, email_id = self._connection.search(None, "SUBJECT", search_key)
            if response == "OK":
                fetch_res, data = self._connection.fetch(email_id[0], "(RFC822)")
                if fetch_res:
                    logging.info(" Email fetched successfully.")
                    result = data
        except Exception as get_id_err:
            logging.error(" Error in %s\n%s", self.__get_email_in_bytes.__name__, get_id_err)
            raise get_id_err
        return result

    def __save_attachment(self, byte_message) -> str:
        """
        Save email attachment inside src/ directory.

        argument:
            byte_message: email message in bytes.
        return:
            file_name: name of file in attachment.

        """
        file_name = None
        try:
            logging.info(" Converting bytes data to normal string.")
            raw_message = message_from_bytes(byte_message)
            for part in raw_message.walk():
                file_name = part.get_filename()
                if bool(file_name):
                    file_path = path.join("src/", file_name)
                    logging.info(" Saving donwload file at %s", file_path)
                    with open(file_path, "wb") as file:
                        file.write(part.get_payload(decode=True))
            logging.info(" Saved file successfully")
        except Exception as save_att_err:
            logging.error(" Error in %s\n%s", self.__save_attachment.__name__, save_att_err)
            raise save_att_err
        return file_name

    def save(self, key: str) -> str:
        """
        This is the only public function,
        from where you can trigger this class.

        argument:
            key: subject, for which you want to search email.
        return:
            name: saved file name.
        """
        name = None
        try:
            logging.info(" Save attachment process started.")
            data = self.__get_email_in_bytes(key)
            name = self.__save_attachment(data[0][1])
            logging.info(" Save attachment process completed. ")
        except Exception as start_err:
            logging.error(" Error in %s\n%s", self.save.__name__, start_err)
            raise start_err
        return name
