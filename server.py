from flask import Flask, send_file
from cv2 import VideoCapture, imwrite

app = Flask(__name__)
cam = VideoCapture(0)

@app.route('/')
def image():
	success, f = cam.read()
	if success:
		imwrite('frame.jpg', f)
	return send_file('frame.jpg', mimetype='image/jpeg')

app.run(host='0.0.0.0')
