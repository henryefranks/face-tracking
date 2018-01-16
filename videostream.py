import numpy as np
import cv2
from threading import Thread
import urllib.request as url

class VideoStream(object):
	def __init__(self, res, ip):
		self.res = res
		self.ip = ip
		self.get_frame()
		self.stopped = False
		
	def start(self):
		t = Thread(target=self.update, args=())
		t.daemon = True
		t.start()

	def get_frame(self):
		server = url.urlopen("http://%s:5000" % self.ip)
		img = np.asarray(bytearray(server.read()), dtype="uint8")
		img = cv2.imdecode(img, cv2.IMREAD_COLOR)
		self.frame = cv2.resize(img, self.res)

	def update(self):
		while True:
			if self.stopped:
				return
			self.get_frame()

	def stop(self):
		self.stopped = True
