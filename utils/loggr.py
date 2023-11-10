# logging.py
import logging
import configparser


# Load config file
config = configparser.ConfigParser()
config.read('./config/config.conf')



def log_error(data, exception, traceback_info):
    logging.basicConfig(filename=config['path']['log'], level=config['log']['log.level'])
    logging.error(f"Data: {data}, Exception: {exception}, Traceback: {traceback_info}")
