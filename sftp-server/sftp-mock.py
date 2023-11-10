# sftp-mock.py
import http.server
import socketserver
import os
import json
import configparser


# Load config file
config = configparser.ConfigParser()
config.read('./config/config.conf')

# Load the server configuration from config.json
with open(config['path']["config.sv"]) as f:
    config_srv = json.load(f)

PORT = config_srv['port.sv']
HOST = config_srv['host.sv']
DATA_DIR = config_srv['path']


# Create a custom request handler to serve log reports and directory listings
class MockRequestHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored. (They should be
        ignored, as they might be unsafe.)

        For example, if `DATA_DIR` is '/sftp-server/data/', and path is
        '/data/report_7.txt', the returned path would be
        '/sftp-server/data/report_7.txt'.
        """
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
                # Serve a modified directory listing with recognizable tags
                listing = self.generate_directory_listing()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(listing.encode('utf-8'))
            else:
                # Serve files from the DATA_DIR directory
                super().do_GET()
        else:
            # Redirect requests to / to show the content of /data/
            self.send_response(302)
            self.send_header('Location', './data')
            self.end_headers()
        
    def do_DELETE(self):
        # Use the translate_path method to get the correct file path
        file_path = self.translate_path(self.path)

        print(f"Attempting to delete: {file_path}")  # Log the file path

        if os.path.isfile(file_path):  # Check if it's an actual file
            try:
                # os.remove(file_path)
                self.send_response(204)
                print(f"Successfully deleted: {file_path}")  # Log successful deletion
            except PermissionError:
                self.send_response(403, "Permission Denied")
                print(f"Permission denied: {file_path}")  # Log permission issues
            except Exception as e:
                self.send_response(500, "Internal Server Error")
                print(f"Error deleting file: {e}")  # Log other exceptions
        else:
            self.send_response(404, "File Not Found")
            print(f"File not found: {file_path}")  # Log if file is not found

        self.end_headers()


    def generate_directory_listing(self):
        # Generate a directory listing with recognizable tags
        file_list = os.listdir(DATA_DIR)
        listing = f'<h1>Directory listing for /data/</h1><hr><ul>\n'
        for file_name in file_list:
            listing += f'<li><a href="{file_name}" data-file="{file_name}">{file_name}</a></li>\n'
        listing += '</ul><hr>'
        return listing

# Start the mock server
with socketserver.TCPServer((HOST, PORT), MockRequestHandler) as httpd:
    print(f"Serving mock data at http://{HOST}:{PORT}")
    httpd.serve_forever()