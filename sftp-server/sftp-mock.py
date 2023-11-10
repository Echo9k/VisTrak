import http.server
import socketserver
import os
import json
import configparser
import logging


# Load config file
config = configparser.ConfigParser()
config.read('./config/config.conf')

# Load the server configuration from config.json
with open(config['path']["config.sv"]) as f:
    config_srv = json.load(f)

PORT = config_srv['port.sv']
HOST = config_srv['host.sv']
DATA_DIR = config['path']['source']
log_file_path = config['path']['log'] + 'sftp_mock.log'

# Configure logging
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a custom request handler to serve log reports and directory listings
class MockRequestHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        tail_part = path.replace('/data/', '', 1)
        return os.path.join(DATA_DIR, tail_part)
    directory = DATA_DIR

    def end_headers(self):
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        super().end_headers()

    def do_GET(self):
        if self.path.startswith("/data/"):
            if self.path == "/data/":
                listing = self.generate_directory_listing()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(listing.encode('utf-8'))
            else:
                super().do_GET()
        else:
            self.send_response(302)
            self.send_header('Location', './data')
            self.end_headers()
        
    def do_DELETE(self):
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


    def generate_directory_listing(self):
        file_list = os.listdir(DATA_DIR)
        listing = f'<h1>Directory listing for /data/</h1><hr><ul>\n'
        for file_name in file_list:
            listing += f'<li><a href="{file_name}" data-file="{file_name}">{file_name}</a></li>\n'
        listing += '</ul><hr>'
        return listing

# Start the mock server
with socketserver.TCPServer((HOST, PORT), MockRequestHandler) as httpd:
    logging.info(f"Serving mock data at http://{HOST}:{PORT}")
    httpd.serve_forever()