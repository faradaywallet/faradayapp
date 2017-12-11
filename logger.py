import datetime
from db_controller import FaradayDB

timestamp = datetime.datetime.now()
db = FaradayDB('localhost', 3310, 'root', 'cybr200', 'faraday') # TODO: Find out a way to hide database connection information

class Logger:

    def log(self, message):
        print(str(timestamp), message)
        db.insert_log(values=(str(timestamp), message))

