##########################
## Face Tracking Client ##
##########################

from __future__ import print_function
import numpy as np
import cv2
from os.path import dirname as pwd
from videostream import VideoStream
import dlib
import face_recognition_models
from os.path import abspath as ap
from os import listdir as ls
from operator import itemgetter
from itertools import repeat
import sys

# IP input
if len(sys.argv) < 2:
	print("Please supply an IP address")
	sys.exit()
else:
	ip = sys.argv[1]
	print("Connecting to server %s:5000" % ip)

print("Initialising...")

def get_dist(name, known_encodings, unknown_encoding):
	# Distance between known and unknown faces
    matches = list(np.linalg.norm(known_encodings[name] - unknown_encoding, axis=1))
    return name, float(sum(matches)) / len(matches)

def face_encoding(face_image, predictor, encoder):
	# Generate encoding for face
	raw_landmark_set = predictor(face_image, dlib.rectangle(0, 0, face_image.shape[0], face_image.shape[1]))
	return np.array(encoder.compute_face_descriptor(face_image, raw_landmark_set, 1))

def detect_faces(cascade, image):
	# Haar cascade detection
	return cascade.detectMultiScale(
		image,
		scaleFactor=1.1,
		minNeighbors=5,
		minSize=(30, 30),
		flags = cv2.CASCADE_SCALE_IMAGE
	)

frame = 0
loc = pwd(ap(__file__))
size = (640, 360)

# Getting list of people
people = ls(loc + "/faces") # Scanning 'faces' folder for people
if ".DS_Store" in people:
	people.remove(".DS_Store")
known_encodings = {}
names = {}
text_cache = []

print("   Initialising face recognition... ", end="")
sys.stdout.flush()
face_detector = dlib.get_frontal_face_detector()
predictor_5_point_model = face_recognition_models.pose_predictor_five_point_model_location()
pose_predictor = dlib.shape_predictor(predictor_5_point_model) # 5 point pose predictor
face_recognition_model = face_recognition_models.face_recognition_model_location()
face_encoder = dlib.face_recognition_model_v1(face_recognition_model)
print("Done!")

print("   Initialising OpenCV... ", end="")
sys.stdout.flush()
cam = VideoStream(size, ip)
face_cascade = cv2.CascadeClassifier("%s/classifiers/face.xml" % loc)
profile_cascade = cv2.CascadeClassifier("%s/classifiers/profile.xml" % loc)
font = cv2.FONT_HERSHEY_SIMPLEX
print("Done!")

print("   Initialising face data... ", end="")
sys.stdout.flush()
for name in people: # Generate encoding for all known faces before scanning
	path = loc + "/faces/" + name
	if len(ls(path)) > 1:
		known = [cv2.imread(path + "/" + file)[:, :, ::-1] for file in ls(path) if file != ".DS_Store"]
		known_encodings[name] = [face_encoding(img, pose_predictor, face_encoder) for img in known]
print("Done!")

print("Initialisation complete, starting webcam...")

try:
	cam.start()
	print("Press Enter to quit")
	while cv2.waitKey(1) != 13:
		img = cam.frame
		bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		faces = detect_faces(face_cascade, bw)

		if frame & 1: # Clear cache or print cached faces
			text_cache = []
		else:
			for name, pos in text_cache:
				cv2.putText(
					img,
					name, pos,
					font,1, (0, 0, 0),
					2, cv2.LINE_AA
				)

		for i, face in enumerate(faces):
			x, y, w, h = face
			if frame & 1: # Only update faces every other frame to increase speed
				matches = {}
				crop = img[y:y+h, x:x+w, ::-1]

				unknown_encoding = face_encoding(crop, pose_predictor, face_encoder)
				names = {key:value for key, value in map(get_dist,
					known_encodings.keys(),
					repeat(known_encodings),
					repeat(unknown_encoding)
					)}

				crop_string = "Face %d" % i

				if any(s <= 0.6 for s in names.values()):
					# Find most likely name for face
					name = min(names.items(), key=itemgetter(1))[0]
					cv2.putText( # Print name on frame
						img,
						name,
						(x + 10, y + h - 15),
						font, 1, (0, 0, 0),
						2, cv2.LINE_AA
					)
					text_cache.append((name, (x + 10, y + h - 15))) # Cache for next frame 
					crop_string += ": %s" % name

			cv2.rectangle( # Rectangle around face
				img,
				(x, y),
				(x+w, y+h),
				(0, 0, 0),
				2
			)

		cv2.imshow("Faces", img)
		frame += 1

except KeyboardInterrupt:
	# Exit properly after ctrl-c
	print(" Keyboard Interrupt")

print("Exiting...")
cam.stop()
cv2.destroyAllWindows()
