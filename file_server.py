import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
import mimetypes
import urllib.parse

# Set the directory to store uploaded files
UPLOAD_DIR = "uploads"
STATIC_DIR = "static"

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Define the host and port
host = "192.168.12.24"  # Note use your own Ip address for this to work,You can also use 'localhost' if you're testing on the same machine.
port = 8000 #if port 8000 is occupied , you can change it to 8001, 8002, etc.

class FileSharingHTTP(BaseHTTPRequestHandler):

    def do_GET(self):
        """Handle GET requests: List available files and serve them"""
        if self.path == "/":
            self.list_files()
        elif self.path.startswith("/static/"):
            self.serve_static_file()
        else:
            # Serve a specific file for download
            self.download_file()

    def do_POST(self):
        """Handle POST requests: File upload and deletion"""
        if self.path == "/upload":
            self.upload_file()
        elif self.path == "/delete":  # New condition for file deletion
            self.delete_file()

    def list_files(self):
        """List all uploaded files in the uploads folder"""
        files = os.listdir(UPLOAD_DIR)
        files_html = "".join(f"<li><a href='/{urllib.parse.quote(file)}'>{file}</a> <form action='/delete' method='POST'><input type='hidden' name='filename' value='{urllib.parse.quote(file)}'><button type='submit'>Delete</button></form></li>" for file in files)
        
        # Read index.html file and inject the file list
        with open("index.html", "r") as f:
            html_content = f.read()
        
        html_content = html_content.replace("<!-- Files will be listed here dynamically -->", files_html)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(html_content, "utf-8"))

    def serve_static_file(self):
        """Serve static files like CSS"""
        file_path = self.path.lstrip("/")
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            if file_path.endswith(".css"):
                self.send_header("Content-type", "text/css")
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, "File Not Found")

    def delete_file(self):
        """Handle file deletion"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = post_data.decode('utf-8')
        form =  urllib.parse.parse_qs(post_data)
        filename = urllib.parse.unquote(form.get('filename', [''])[0])
        file_path = os.path.join(UPLOAD_DIR, filename)

        try:
            os.remove(file_path)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(f"<html><body><h1>File '{filename}' deleted successfully!</h1></body></html>", "utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(f"<html><body><h1>Error deleting file: {e}</h1></body></html>", "utf-8"))

    def upload_file(self):
        """Handle file upload"""
        # Get the content type of the request (it should be multipart form data)
        ctype, pdict = cgi.parse_header(self.headers.get('Content-Type'))
        if ctype != 'multipart/form-data':
            self.send_error(400, "Invalid Content-Type")
            return
        
        # Parse the form data
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
        
        # Extract the file from the form data
        if "file" not in form:
            self.send_error(400, "No file part")
            return
        
        uploaded_file = form["file"]
        if uploaded_file.filename:
            file_path = os.path.join(UPLOAD_DIR, uploaded_file.filename)
            # Save the file to the upload directory
            with open(file_path, "wb") as f:
                f.write(uploaded_file.file.read())

            # Confirm upload success
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(f"<html><body><h1>File uploaded successfully!</h1></body></html>", "utf-8"))
        else:
            self.send_error(400, "No file selected")

    def download_file(self):
        """Handle downloading a file"""
        filename = urllib.parse.unquote(self.path.strip("/")) 
        file_path = os.path.join(UPLOAD_DIR, filename)

        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                content = f.read()

            self.send_response(200)
            
            # Guess the MIME type based on the file extension
            content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream" 

            self.send_header("Content-type", content_type)
            self.send_header("Content-Disposition", f"attachment; filename={filename}")
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, "File not found")

# Set up the server and start it
server = HTTPServer((host, port), FileSharingHTTP)
print(f"Server running at http://{host}:{port}/")
server.serve_forever()
