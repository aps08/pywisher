"""
This module is responsible for sending email, to friend
with wishes, along with that it will also send
you a reminder.
"""

import logging
import logging.config
import smtplib
import sys
from email.message import EmailMessage

sys.dont_write_bytecode = True

logging.config.fileConfig("src/logging.conf")


class SendEmailService:
    """This class is responsible for sending email."""

    def __init__(self, username: str, password: str):
        """Constructor"""
        self._username = username
        self._password = password
        self._domain = "smtp.gmail.com"
        self._port = 587
        logging.info(" %s class is initialised.", SendEmailService.__name__)

    def __create_message(self, email_to: str, subject: str) -> EmailMessage:
        """
        Creates the emails for sending.

        argument:
            email_to: receiver of the email.
            subject: subject of the email.
        return:
            create_message: object of type EmailMessage,
                            containing all info.
        """
        create_message = None
        try:
            logging.info(" Creating a message.")
            create_message = EmailMessage()
            create_message["From"] = self._username
            create_message["To"] = email_to
            create_message["Subject"] = subject
            mail_content = "Custom mail, content"
            create_message.set_content(mail_content)
        except Exception as cre_err:
            logging.error(" Error in %s\n%s", self.__create_message.__name__, cre_err)
            raise cre_err
        logging.info(" Returning the message")
        return create_message

    def __send__created_email(self, wish_message: EmailMessage, email_to: str) -> None:
        """
        Create a smtp session, and sends the email.

        argument:
            wish_messsage: Complete message to be sent.
            email_to: receiver of the email.
        """
        try:
            logging.info(" Creating a session for sending email.")
            session = smtplib.SMTP(self._domain, self._port)
            session.starttls()
            session.login(self._username, self._password)
            session.sendmail(self._username, email_to, wish_message.as_bytes())
            logging.info(" Email sent, quiting the session.")
            session.quit()
        except Exception as sen_cre_err:
            logging.error(" Error in %s\n%s", self.__send__created_email.__name__, sen_cre_err)
            raise sen_cre_err

    def send(self, receiver: str, wtype: str) -> None:
        """
        This is the only public function,
        from where you can trigger this class.

        argument:
            receiver: receiver of the email.
            wtype: wish type
        """
        try:
            logging.info(" Sending email process started.")
            created_message = self.__create_message(receiver, wtype)
            self.__send__created_email(created_message, self._username)
            logging.info(" Sending email process completed.")
        except Exception as send_err:
            logging.error(" Error in %s\n%s", self.send.__name__, send_err)
            raise send_err
