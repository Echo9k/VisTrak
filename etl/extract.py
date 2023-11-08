import configparser
import requests
from bs4 import BeautifulSoup
import os
import json
import zipfile  # Import the zipfile module for creating ZIP archives

# Read the config file for the ETL process
config = configparser.ConfigParser()
config.read("/workspaces/anaconda-postgres/config/config.conf")


# Read the config file for the mock server
with open(config['source']['config_file']) as f:
    config_server = json.load(f)

# Define the URL of the mock server
mock_server_url = f"http://{config_server['host']}:{config_server['port']}/{config_server['path']}/"

# Send an HTTP GET request to the mock server
response = requests.get(mock_server_url)

if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all <a> elements with the data-file attribute
    file_links = soup.find_all("a", {"data-file": True})
    # Directory to save the downloaded files
    download_dir = config['source']['download_dir']
    backup_dir = config['source']['backup_dir']  # Get the backup directory path from the config

    # Create the download and backup directories if they don't exist
    os.makedirs(download_dir, exist_ok=True)
    os.makedirs(backup_dir, exist_ok=True)

    # Loop through the file links
    for link in file_links:
        file_name = link["data-file"]
        if file_name.startswith("report_") and file_name.endswith(".txt"):
            file_url = mock_server_url + file_name
            file_path = os.path.join(download_dir, file_name)

            # Download the file
            file_response = requests.get(file_url)
            if file_response.status_code == 200 and file_response.content:
                with open(file_path, "wb") as file:
                    file.write(file_response.content)
                print(f"Downloaded: {file_name}")

                # Backup the file in ZIP format
                zip_file_path = os.path.join(backup_dir, f"{file_name}.zip")
                with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(file_path, arcname=file_name)
                print(f"Backed up: {file_name} in ZIP format at {zip_file_path}")

                # Attempt to delete the file from the mock server
                delete_response = requests.delete(file_url)
                if delete_response.status_code == 204:
                    print(f"Deleted: {file_name} from the server")
                else:
                    print(f"Failed to delete: {file_name} from the server with status code: {delete_response.status_code}")
                    print(f"Error message: {delete_response.text}")
            else:
                print(f"Failed to download: {file_name}")
else:
    print(f"Failed to fetch the mock server page with status code: {response.status_code}")