# OpenCV Face Tracking and Recognition
A tech demo of face tracking and recognition using OpenCV.

## Setup
##### To install:
`pip install -r requirements.txt`

##### To run:
`python server.py` to use the SimpleHTTPServer backend
`python flask.py` to use the Flask backend
*Note: there is no difference in functionality between the backends, the choice is down to user preference*

`python client_test.py` to view a direct stream from the webcam
`python tracking.py` for facial recognition.

### Facial Recognition
Faces are found using a standard OpenCV classifier. By adding photos of a face to the `faces/` directory under a named subfolder, the software can recognise and identify the face on the stream. For example, If a face detected on the stream found a match against photos in the `faces/John` folder, it would identify the face as John.

To allow the software to recognise your face, simply create a folder with your name in the `faces/` directory and add photos of yourself.
