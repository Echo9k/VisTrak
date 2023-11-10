import os
import sys
import json
import psycopg2
import configparser


# Load config file
config = configparser.ConfigParser()
config.read('./config/config.conf')

# Load configuration file (json format) for source database 
with open(config['path']['config.sv']) as json_file:
    source = json.load(json_file)

# Load configuration file (json format) for target database
DATA_DIR = config['path']['data']
HOST = config['database']['host.sv']
PORT = config['database']['port.sv']
paths = config['path']
temp_dir = paths['temp']

# Add root directory to sys.path
# This is necessary in my environment
sys.path.append(config['path']['root'])
from utils import (insert as insert, parse as parse, process, validate as validate)


# Connect to Postgres database
cnx = psycopg2.connect(
    database=source['database'],
    user=source['user'],
    password=source['password'],
    host=source.get('host', 'localhost'),  # 'localhost' as default
    port=source.get('port', '5432')  # '5432' is postgres' default
)


# Usage
temp_dir = paths['temp']
for filename in os.listdir(temp_dir):
    print(filename)
    if filename.endswith('.txt'):
        full_path = os.path.join(temp_dir, filename)
        process.process_file(full_path, cnx)
        os.remove(full_path)


# Close Postgres connection
cnx.close()