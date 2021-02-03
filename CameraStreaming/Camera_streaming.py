#!/usr/bin/env python

import cv2 as cv
import numpy as np
import threading
import datetime
import time

from flask import Response
from flask import Flask
from flask import render_template

app = Flask(__name__)
cam = cv.VideoCapture(0)
# cam = cv.VideoCapture(-1)
time.sleep(3)
cam.set(3, 640) #Width
cam.set(4, 480) #Height
outputFrame = None

def ImageCapture():
	# grab global references to the output frame and lock variables
	global outputFrame

    # loop over frames from the output stream
	while True:
		ret,outputFrame = cam.read()
		
		# check if the output frame is available, otherwise skip
		# the iteration of the loop
		if outputFrame is None:
			continue

		# encode the frame in JPEG format
		(flag, encodedImage) = cv.imencode(".jpg", outputFrame)
		encodedImage = encodedImage.tobytes()
		# ensure the frame was successfully encoded
		if not flag:
			continue
		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
			encodedImage + b'\r\n')



@app.route('/')
def index():
	# return the rendered template
	return render_template("index.html")

@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(ImageCapture(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__ == '__main__':
	# t = threading.Thread(target=ImageCapture)
	# t.daemon = True
	# t.start()
	app.run(host='0.0.0.0', debug=False,
	   threaded=True, use_reloader=False)
cam.release()
