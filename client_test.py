###############################
## OpenCV Client Test Script ##
###############################

from __future__ import print_function
import cv2
import urllib.request as url
import numpy as np
import sys

# IP input
if len(sys.argv) < 2:
        print("Please supply an IP address")
        sys.exit()
else:
        ip = sys.argv[1]
        print("Connecting to server %s:5000" % ip)

while cv2.waitKey(1) != 13:
	# Download and show image
	resp = url.urlopen("http://%s:5000" % ip)
	img = np.asarray(bytearray(resp.read()), dtype="uint8")
	img = cv2.imdecode(img, cv2.IMREAD_COLOR)

	cv2.imshow("Client Test", img)
