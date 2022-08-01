"""
module doc stirng
"""
import sys
from service import Service

sys.dont_write_bytecode = True

service = Service()
drive = service.get_drive()
file_object = drive.CreateFile(metadata={"id": service.get_file_id()})
file_object.GetContentFile(filename="src/file.csv")
