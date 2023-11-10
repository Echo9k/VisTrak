# transform.py
import os
import sys
import configparser
import logging
from tqdm import tqdm


# Load config file
config = configparser.ConfigParser()
config.read('./config/config.conf')
sys.path.append(".")
from utils import processing as process


# Define the path to the raw data folder and temp output folder
raw_data_folder = config['path']['raw']
temp_output_folder = config['path']['temp']
path_logs = config['path']['log'] + 'transform.log'

# Configure logging
logging.basicConfig(filename=path_logs, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Process each file in the raw data directory
files_in_folder = os.listdir(raw_data_folder)
success_counter = 0

# Use tqdm to show a progress bar
for filename in tqdm(files_in_folder):
    if filename.endswith('.txt'):
        file_path = os.path.join(raw_data_folder, filename)
        output_file_path = os.path.join(temp_output_folder, filename)  # Output path in the temp folder
        process.process_file(file_path, output_file_path)  # Process the file and create the output

        # Log processing information
        logging.info(f"Processed: {file_path}")
        logging.info(f"Output: {output_file_path}")

        # Delete the processed file from the raw data folder
        try:
            os.remove(file_path)
            logging.info(f"Deleted: {file_path}")
            success_counter += 1
        except Exception as e:
            logging.error(f"Failed to delete: {file_path}: {e}")

# Log a summary at the end
logging.info(f"Data transformation and validation completed.\t{success_counter}/{len(files_in_folder)}")
