import logging
import os

class Log():
    def __init__(self):
        filename = os.path.join(os.getcwd(), 'core')
        filename = os.path.join(filename, 'log.txt')
        logging.basicConfig(filename=filename, level=logging.INFO)
    
    def logNormal(self, string):
        logging.info(string)
    
    def logError(self, error, code):
        logging.error("ERR: {}! ON {}.".format(error, code))