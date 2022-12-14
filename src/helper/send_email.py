"""
This module is responsible for sending email, to friend
with wishes, along with that it will also send
you a reminder.
"""

import logging
import logging.config
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sys.dont_write_bytecode = True
logging.config.fileConfig("logging.conf")


class SendEmailService:
    """This class is responsible for sending email."""

    def __init__(self, username: str, password: str):
        """Constructor"""
        self._username = username
        self._password = password
        self._domain = "smtp.gmail.com"
        self._port = 587
        logging.info(" %s class is initialised.", SendEmailService.__name__)

    def __create_message(self, emails_to: str, subject: str) -> MIMEMultipart:
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
            create_message = MIMEMultipart()
            create_message["From"] = self._username
            create_message["To"] = emails_to
            create_message["Subject"] = subject
            mail_content = ""
            with open(file="templates/sample.html", mode="r", encoding="utf-8") as file_obj:
                mail_content = file_obj.read()
            create_message.attach(MIMEText(mail_content, "html"))
        except Exception as cre_err:
            logging.error(" Error in %s\n%s", self.__create_message.__name__, cre_err)
            raise cre_err
        logging.info(" Returning the message")
        return create_message

    def __send__created_email(self, wish_message: MIMEMultipart, email_to: str) -> None:
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
            session.sendmail(self._username, email_to, wish_message.as_string())
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
            wtype: wish type, default birthday
        """
        try:
            created_message = self.__create_message(receiver, wtype)
            self.__send__created_email(created_message, receiver)
        except Exception as send_err:
            logging.error(" Error in %s\n%s", self.send.__name__, send_err)
            raise send_err
        logging.shutdown()
