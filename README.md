# OpenCV Face Tracking and Recognition

The software runs as a server so any device on the network can view the stream. There are two options for the server backend: SimpleHTTPServer (`server.py`) or Flask (`flask.py`). The device running the server must be connected to the webcam to be used.

On the client, run `client_test.py` to view a direct stream from the webcam or `tracking.py` for facial recognition.

### Facial Recognition
Faces are found using a standard OpenCV classifier. By adding photos of a face to the `faces/` folder under a named subfolder, the software can recognise and identify the face on the webcam. For example, If a face detected on the webcam found a match against photos in the `faces/John` folder, it would identify the face as John.
