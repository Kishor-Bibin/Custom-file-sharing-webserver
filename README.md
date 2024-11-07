# Custom-file-sharing-webserver
# Simple Python File Server

This is a basic file server implemented in Python using the `http.server` module. It allows you to upload, download, and delete files through a web interface.

## Features

* **File uploading:** Upload files through a simple form.
* **File downloading:** Download uploaded files with correct MIME types.
* **File deletion:** Delete uploaded files with a click of a button.
* **File listing:** View a list of all uploaded files.
* **Basic styling:** Includes CSS for a clean and user-friendly interface.

## How to run

1. **Clone the repository:** `git clone https://github.com/your-username/your-repository.git`
2. **Install dependencies:** This project has no external dependencies.
3. **Run the server:** `python file_server.py`
4. **Access the server:** Open your web browser and go to `http://192.168.1.34:8000/` (replace with your server's IP address and port if needed).

## Code overview

* **`file_server.py`:** Contains the Python code for the file server.
    * `UPLOAD_DIR`: Specifies the directory where uploaded files are stored.
    * `STATIC_DIR`: Specifies the directory for static files (CSS, etc.).
    * `FileSharingHTTP`: Class that handles HTTP requests.
        * `do_GET`: Handles GET requests for listing files, serving static files, and downloading files.
        * `do_POST`: Handles POST requests for uploading and deleting files.
* **`index.html`:** The main HTML file for the web interface.
* **`static/style.css`:** CSS file for styling the web interface.

## Contributing

Feel free to contribute to this project by submitting issues or pull requests.

