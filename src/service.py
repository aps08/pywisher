"""
This module is responsible for creating the service object for connecting to
google cloud APIs.
Uses: client_secrets.json file
"""
import sys

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

sys.dont_write_bytecode = True


class Service:
    """Creates the service object"""

    def __init__(self) -> None:
        """constructor"""
        self._gauth = GoogleAuth()
        self._scopes = [
            "https://www.googleapis.com/auth/drive.readonly",
            "https://www.googleapis.com/auth/gmail.send",
        ]
        self._gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            "src/secrets.json", self._scopes
        )
        self._file_id = "1ZoKpvWGRHk4XJ3iYXaYAomYbzx5GeRVQ"

    def get_drive(self):
        """returns google drive object"""
        drive = GoogleDrive(self._gauth)
        return drive

    def get_gmail(self):
        """returns google gmail object"""
        service = build("gmail", "v1", credentials=self._gauth.credentials)
        return service

    def get_file_id(self):
        """returns file id"""
        return self._file_id
