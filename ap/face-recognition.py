"""
Face Recognise Module
Check from the encoded file if any saved image match the face income
Acknowledgement
This code is adapted from:
https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/
"""

import pickle
import time

import cv2
import face_recognition
import imutils
# import the necessary packages
from imutils.video import VideoStream


class FaceId:
    """
    Provide the static recognise method
    identified by username and matched face
    """

    @staticmethod
    def recognise(username):
        """
        Compare the username with the recorded user face database
        :param username: username that need to compare with the saved images
        :return: True if matched any
        :rtype bool
        """
        # load the known faces and embeddings
        print("[INFO] Loading Face Dataset...")
        data = pickle.loads(open("encodings.pickle", "rb").read())

        # initialize the video stream and then allow the camera sensor to warm up
        print("[INFO] Starting Video Stream...")
        video_stream = VideoStream(src=0).start()
        time.sleep(2.0)

        attempt_count = 0
        while attempt_count <= 10:
            # grab the frame from the threaded video stream
            frame = video_stream.read()

            # convert the input frame from BGR to RGB then resize it to have
            # a width of 750px (to speedup processing)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb = imutils.resize(frame, width=240)

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input frame, then compute
            # the facial embeddings for each face
            boxes = face_recognition.face_locations(rgb, model="hog")
            encodings = face_recognition.face_encodings(rgb, boxes)
            names = []

            # loop over the facial embeddings
            for encoding in encodings:
                # attempt to match each face in the input image to our known
                # encodings
                matches = face_recognition.compare_faces(data["encodings"], encoding)
                name = "Unknown"

                # check to see if we have found a match
                if True in matches:
                    # find the indexes of all matched faces then initialize a
                    # dictionary to count the total number of times each face
                    # was matched
                    matched_index = [i for (i, b) in enumerate(matches) if b]
                    counts = {}

                    # loop over the matched indexes and maintain a count for
                    # each recognized face face
                    for i in matched_index:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1

                    # determine the recognized face with the largest number
                    # of votes (note: in the event of an unlikely tie Python
                    # will select first entry in the dictionary)
                    name = max(counts, key=counts.get)

                # update the list of names
                names.append(name)

            # loop over the recognized faces
            if username in names:
                # release the camera resource
                video_stream.stop()
                return True
            time.sleep(1.0)
            attempt_count += 1

        # do a bit of cleanup
        video_stream.stop()
        print("Can't find the matched face data")
        return False