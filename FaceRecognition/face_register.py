import cv2
import numpy
import face_recognition
from FaceRecognition.face_database import FaceDatabase
import time
from config import config


'''
This class is used to register a face into the database
Ie. Saving an image of a face to the dataset
'''


class FaceRegisterer:
    class NoImageDetectedException(Exception):
        pass

    def __init__(self, dirname):
        self.__dirname = dirname    # This is the path of our face dataset
        self.__db = FaceDatabase(dirname)

    @staticmethod
    def if_face_detected(frame):
        locations = face_recognition.face_locations(frame)
        return len(locations) > 0

    # This method uses a webcam to register a face to the dataset
    # After a duration specified by time_out or if user presses the stop_key, if no face is discovered
    # nothing will be registered to our dataset
    def capture(self, name="Unknown", time_out=10, stop_key='e'):
        # Open camera
        video_capture = cv2.VideoCapture(0) # Use the default webcam on the device

        # Set start time to calculate the elapsed time
        start = time.time()
        while True:
            ret, frame = video_capture.read()
            cv2.imshow("Webcam", frame) # Show to webcam windows
            stop = time.time()  # Get stop time to calculate elapsed time

            # If user presses the stop key or timed out, we will stop immediately
            if cv2.waitKey(1) & 0xFF == ord(stop_key) or stop - start > time_out:
                # Save image into the dataset, only if there is an image detected
                if FaceRegisterer.if_face_detected(frame):
                    self.__db.save(frame, name)
                else:
                    # Release webcam and clear its windows
                    video_capture.release()
                    cv2.destroyAllWindows()
                    # We will throw an exception if there is no face detected after timed_out or quit
                    raise FaceRegisterer.NoImageDetectedException("No image detected")
                break

        # Release webcam and clear its windows
        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    rg = FaceRegisterer(config["dataset"])
    try:
        rg.capture(name="John")
    except Exception as e:
        print(e)
