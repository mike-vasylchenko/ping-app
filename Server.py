import sys
import configparser
from multiprocessing import Process
from flask import Flask
import requests
from time import sleep
import ast
import hashlib

app = Flask(__name__)
confFile = "./config/config.cfg"

@app.route("/ping")
def ping():
    return "pong\n"

@app.route("/check-hosts")
def startCheck():
    parser = configparser.ConfigParser()
    parser.read(confFile)

    hash = hash_file(confFile)

    hosts = ast.literal_eval(parser.get("config", "hosts"))
    calls = int(parser.get("config", "calls_per_minute"))

    for host in hosts:
        p = Process(target=restGet, args=(host, calls, hash))
        p.daemon = True
        p.start()

    return "started\n"

def restGet(url, calls, hash):
    logger = create_logger()
    while hash == hash_file(confFile):
        response = requests.get(url)

        if response.status_code == 200:
            logger.info("URL: " + url + "; Status Code: " + str(response.status_code))
            if 'pong' not in str(response.content):
                logger.warning("content doesn't include 'pong'")
        else:
            logger.warning("URL: " + url + "; Status Code: " + str(response.status_code))
        sleep(60 / calls)


def create_logger():
    import multiprocessing, logging
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(\
        '[%(asctime)s| %(levelname)s| %(processName)s] %(message)s')

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    #handler = logging.FileHandler('logs/logs.log')
    #handler.setFormatter(formatter)

    if not len(logger.handlers):
        logger.addHandler(handler)
    return logger

def hash_file(filename):
   """"This function returns the SHA-1 hash
   of the file passed into it"""

   # make a hash object
   h = hashlib.sha1()

   # open file for reading in binary mode
   with open(filename,'rb') as file:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest()


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=80)