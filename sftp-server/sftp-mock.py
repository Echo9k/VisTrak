import http.server
import logging
import socketserver
import os

from etl.load import DATA_DIR
from utils.helpers import read_config_file


class MockRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    MockRequestHandler
    A custom request handler for the mock server.
    """

    def __init__(self, *args, **kwargs):
        self.directory = DATA_DIR
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


paths = read_config_file('./config/config.conf')['path']

PORT = paths['port.sv']
HOST = paths['host.sv']

# Start the mock server
with socketserver.TCPServer((HOST, PORT), MockRequestHandler) as httpd:
    logging.info(f"Serving mock data at http://{HOST}:{PORT}")
    httpd.serve_forever()
