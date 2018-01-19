######################
## SimpleHTTPServer ##
######################

from __future__ import print_function
from http.server import SimpleHTTPRequestHandler
import socketserver
import socket
import os
import threading
from cv2 import VideoCapture, imencode

class Handler(SimpleHTTPRequestHandler):
    cam = VideoCapture(0)

    def do_GET(self):
        # Return image for GET request
        self.send_response(200)
        self.send_header("Content-type", "image/jpg")
        self.end_headers()
        success, img = self.cam.read() # Get image
        if success:
            self.wfile.write(imencode('.jpg', img)[1])

class Server(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, address, handler):
        # Server init
        self.allow_reuse_address = True
        socketserver.TCPServer.__init__(self, address, handler, False)

if __name__ == "__main__":
    # Only run server on main thread
    server = Server(("0.0.0.0", 5000), Handler)
    server.server_bind()
    server.server_activate()
    server_thread = threading.Thread(target=server.serve_forever) # Run server as background thread
    server_thread.start()
    print("Server started on %s:5000" % socket.gethostbyname(socket.gethostname()))
