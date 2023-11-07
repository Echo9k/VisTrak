import requests
from bs4 import BeautifulSoup
import os

# Define the URL of the mock server
mock_server_url = "http://localhost:8000/data/"

# Send an HTTP GET request to the mock server
response = requests.get(mock_server_url)

if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all <a> elements with the data-file attribute
    file_links = soup.find_all("a", {"data-file": True})

    # Directory to save the downloaded files
    download_dir = "/home/vinkOS/archivosVisitas/"

    # Create the download directory if it doesn't exist, and paths if necessary
    os.makedirs(download_dir, exist_ok=True)

    # Loop through the file links
    for link in file_links:
        file_name = link["data-file"]
        file_url = mock_server_url + file_name
        file_path = os.path.join(download_dir, file_name)

        # Download the file
        response = requests.get(file_url)
        if response.status_code == 200:
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"Downloaded: {file_name}")

            # Delete the file from the mock server
            delete_response = requests.delete(file_url)
            if delete_response.status_code == 204:
                print(f"Deleted: {file_name} from the server")
            else:
                print(f"Failed to delete: {file_name} from the server")

        else:
            print(f"Failed to download: {file_name}")
else:
    print("Failed to fetch the mock server page.")
