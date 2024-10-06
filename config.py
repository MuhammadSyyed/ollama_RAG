import os
from datetime import datetime

UI_URL = "http://localhost:3000"

# define init index
INIT_INDEX = os.getenv('INIT_INDEX', 'false').lower() == 'true'

# vector index persist directory
INDEX_PERSIST_DIRECTORY = os.getenv('INDEX_PERSIST_DIRECTORY', "./data/chromadb")

# target url to scrape
TARGET_URL =  os.getenv('TARGET_URL', "https://open5gs.org/open5gs/docs/")

# http api port
HTTP_PORT = os.getenv('HTTP_PORT', 5050)

# mongodb config host, username, password
MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT = os.getenv('MONGO_PORT', 27017)
MONGO_USER = os.getenv('MONGO_USER', 'testuser')
MONGO_PASS = os.getenv('MONGO_PASS', 'testpass')

def check_message_age(date_string):
    '''This function rectifies repeated messages from rocketChat by checking timestamp of message'''
    given_datetime = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
    current_datetime = datetime.utcnow().timestamp()
    difference = current_datetime - given_datetime
    if difference < 5:
        return True
    return False
