from http.server import SimpleHTTPRequestHandler
import socketserver
import os
import threading
from cv2 import VideoCapture, imencode

class Handler(SimpleHTTPRequestHandler):
    cam = VideoCapture(0)

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "image/jpg")
        self.end_headers()
        success, img = self.cam.read()
        if success:
            self.wfile.write(imencode('.jpg', img)[1])

class Server(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, address, handler):
        self.allow_reuse_address = True
        socketserver.TCPServer.__init__(self, address, handler, False)

if __name__ == "__main__":
    server = Server(("0.0.0.0", 5000), Handler)
    server.server_bind()
    server.server_activate()
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
