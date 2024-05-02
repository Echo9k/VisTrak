# transform.py
import os
import sys
import logging
import traceback
from tqdm import tqdm
import psycopg2

# Custom utilities
from utils import process as process
from utils.loggr import Logger
from utils.helpers import get_path

# Configure logging
module = "log." + os.path.basename(__file__).replace(".py", "")
logger = Logger(module, logging.INFO)
config = logger.config

# Define the path to the raw data folder and temp output folder based on environment variables
base_dir = config["path"]["root"]  # Provide a default base directory
raw_dir = get_path(config, 'raw')
temp_output_folder = get_path(config, 'temp')
log_dir = get_path(config, 'log.transform')

# Ensure directories exist
os.makedirs(raw_dir, exist_ok=True)
os.makedirs(temp_output_folder, exist_ok=True)

# Set up database connection
def get_database_connection():
    try:
        return psycopg2.connect("dbname='database_name' user='username' host='hostname' password='password'")
    except Exception as e:
        logger.log_error("Database connection failed", e, traceback.format_exc())
        return None

# Process files in the directory
def process_files():
    files_in_folder = os.listdir(raw_dir)
    success_counter = 0

    for filename in tqdm(files_in_folder, desc="Processing files"):
        if filename.endswith('.txt'):
            file_path = os.path.join(raw_dir, filename)
            output_file_path = os.path.join(temp_output_folder, filename.replace('.txt', '_processed.txt'))

            cnx = get_database_connection()
            if cnx:
                try:
                    process.process_file(file_path, cnx)  # Process the file and create the output
                    logger.info(f"Processed: {file_path}")
                    logger.info(f"Output: {output_file_path}")

                    os.remove(file_path)
                    logger.info(f"Deleted: {file_path}")
                    success_counter += 1
                except Exception as e:
                    logger.log_error(f"Error processing file: {file_path}", e, traceback.format_exc())
                finally:
                    cnx.close()
            else:
                logging.error(f"Skipped processing due to failed database connection: {file_path}")

    # Log summary
    logging.info(f"Data transformation and validation completed. {success_counter}/{len(files_in_folder)} files processed.")

if __name__ == '__main__':
    process_files()