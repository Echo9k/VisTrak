import http.server
import logging
import socketserver
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from utils.helpers import read_config_file

logging.basicConfig(level=logging.INFO)


class MockRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    MockRequestHandler
    A custom request handler for the mock server.
    """

    def __init__(self, *args, **kwargs):
        # The path to the data directory using the config file
        self.directory = read_config_file('./config/config.conf')['path']['data']
        super().__init__(*args, directory=self.directory, **kwargs)

    def do_DELETE(self):
        """
        Handle the DELETE request.

        Args:
            self

        Returns:
            None
        """
        file_path = self.translate_path(self.path)
        logging.info(f"Attempting to delete: {file_path}")

        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                self.send_response(204)
                logging.info(f"Successfully deleted: {file_path}")
            except PermissionError:
                self.send_response(403, "Permission Denied")
                logging.warning(f"Permission denied: {file_path}")
            except Exception as e:
                self.send_response(500, "Internal Server Error")
                logging.error(f"Error deleting file: {e}")
        else:
            self.send_response(404, "File Not Found")
            logging.warning(f"File not found: {file_path}")

        self.end_headers()


database_config = read_config_file('./config/config.conf')['database']

PORT = int(database_config['port.sv'])
HOST = database_config['host.sv']
# logging port and host for debugging, including data type
logging.debug(f"Host: {HOST}", type(HOST))
logging.debug(f"Port: {PORT}", type(PORT))

# Start the mock server
with socketserver.TCPServer((HOST, PORT), MockRequestHandler) as httpd:
    logging.info(f"Serving mock data at http://{HOST}:{PORT}")
    httpd.serve_forever()
