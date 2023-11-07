import http.server
import socketserver
import os

PORT = 8000  # Choose an available port number
DATA_DIR = "/workspaces/anaconda-postgres/data"  # Path to the directory containing log reports

# Create a custom request handler to serve log reports and directory listings
class MockRequestHandler(http.server.SimpleHTTPRequestHandler):
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
            self.send_header('Location', '/data/')
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
with socketserver.TCPServer(("", PORT), MockRequestHandler) as httpd:
    print(f"Serving mock data at http://localhost:{PORT}")
    httpd.serve_forever()