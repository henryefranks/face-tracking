import cv2
import urllib.request as url
import numpy as np

while cv2.waitKey(1) != 13:
	resp = url.urlopen("http://127.0.0.1:5000")
	img = np.asarray(bytearray(resp.read()), dtype="uint8")
	img = cv2.imdecode(img, cv2.IMREAD_COLOR)

	cv2.imshow("Client Test", img)
