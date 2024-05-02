import os
import sys
import json
import tqdm
import psycopg2

import logging
import psycopg2

# Custom utilities
from utils import process as process
from utils.loggr import Logger
from utils.helpers import get_conf_info, get_path

# Configure logging
module = "log." + os.path.basename(__file__).replace(".py", "")
logger = Logger(module, logging.INFO)
config = logger.config

# Load configuration file (json format) for target database
base_dir = config["path"]["root"]
HOST = get_conf_info(config, 'host.sv', section='database')
PORT = get_conf_info(config, 'port.sv', section='database')
temp_dir = get_path(config, 'temp')

# Define the path to the raw data folder and temp output folder based on environment variables
base_dir = config["path"]["root"]  # Provide a default base directory
raw_dir = get_path(config, 'raw')
temp_output_folder = get_path(config, 'temp')
log_dir = get_path(config, 'log.transform')

# Load configuration file (json format) for source database 
with open(get_path(config, 'config.sv')) as json_file:
    source = json.load(json_file)

# Ensure directories exist
os.makedirs(raw_dir, exist_ok=True)
os.makedirs(temp_output_folder, exist_ok=True)



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


# Usage of process.process_file() function
if temp_dir:
    files_in_folder = os.listdir(temp_dir)
    print("Files to load:", len(files_in_folder))
    for filename in tqdm.tqdm(files_in_folder, desc="Processing files"):
        print(filename)
        if filename.endswith('.txt'):
            full_path = os.path.join(temp_dir, filename)
            process.process_file(full_path, cnx)
            os.remove(full_path)

    print("✅ Done loading files")
else:
    print("No files to load")

print("😊 load.py is complete")
# Close Postgres connection
cnx.close()