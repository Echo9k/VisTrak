import configparser
import requests
from bs4 import BeautifulSoup
import os
import json
import zipfile
import logging


# Read the config file for the ETL process
config = configparser.ConfigParser()
config.read("./config/config.conf")

# Configure logging
log_dir = config['path']['log']+"extract.log"
logging.basicConfig(filename=log_dir, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

source_dir = config['path']['source']
raw_dir = config['path']['raw']
backup_dir = config['path']['backup']
logging.info(f"Source directory: {source_dir}")
logging.info(f"Raw directory: {raw_dir}")

# Read the config file for the mock server
with open(config['path']['config.sv']) as f:
    config_server = json.load(f)

logging.info("Downloading files from the mock server...")
mock_server_url = f"http://{config_server['host.sv']}:{config_server['port.sv']}/{config_server['path']}/"

response = requests.get(mock_server_url)
logging.info(f"Response status code: {response.status_code}")

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    file_links = soup.find_all("a", {"data-file": True})
    logging.info(f"Found {len(file_links)} files")

    for link in file_links:
        file_name = link["data-file"]
        logging.info(f"Found file: {file_name}")
        if file_name.startswith("report_") and file_name.endswith(".txt"):
            file_url = mock_server_url + file_name
            file_path = os.path.join(raw_dir, file_name)
            logging.info(f"Downloading: {file_name}")

            if not os.path.exists(raw_dir):
                try:
                    os.makedirs(raw_dir)
                except Exception as e:
                    logging.error(f"Error creating directory {raw_dir}: {e}")

            if not os.path.exists(backup_dir):
                try:
                    os.makedirs(backup_dir)
                except Exception as e:
                    logging.error(f"Error creating directory {backup_dir}: {e}")

            file_response = requests.get(file_url)
            if file_response.status_code == 200 and file_response.content:
                with open(file_path, "wb") as file:
                    file.write(file_response.content)
                logging.info(f"Downloaded: {file_name}")

                zip_file_path = os.path.join(backup_dir, f"{file_name}.zip")
                with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(file_path, arcname=file_name)
                logging.info(f"Backed up: {file_name} in ZIP format at {zip_file_path}")

                delete_response = requests.delete(file_url)
                if delete_response.status_code == 204:
                    logging.info(f"Deleted: {file_name} from the server")
                else:
                    logging.warning(f"Failed to delete: {file_name} from the server with status code: {delete_response.status_code}")
                    logging.error(f"Error message: {delete_response.text}")
            else:
                logging.error(f"Failed to download: {file_name}")
else:
    logging.error(f"Failed to fetch the mock server page with status code: {response.status_code}")