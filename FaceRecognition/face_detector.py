import cv2
import face_recognition
from FaceRecognition.face_database import FaceDatabase
import time
import ntpath
from config import config


'''
This class is used to recognize all known faces saved in the face dataset
'''


class FaceDetector:
    # We use a face database to gather all known face encodings
    def __init__(self, dataset):
        self.__db = FaceDatabase(dataset)

    # This method takes the path of an image containing a face
    # and return the face name without any extension
    # For instance, passing in hello/path/Phat.png will return Phat only
    @staticmethod
    def get_target_name(file_path):
        file_name = ntpath.basename(file_path)
        tokens = file_name.split('.')
        return tokens[0] if len(tokens) > 0 else None

    # This method uses a webcam to detect known faces
    # After a duration specified by time_out or if user presses the stop_key, if no face is discovered
    # nothing will be returned
    def detect(self, time_out=10, stop_key='q'):
        # Create video capture
        video_capture = cv2.VideoCapture(0)

        # Generate known face encodings and their names saved in the dataset
        # using the database object
        known_names = None
        known_encodings = None
        try:
            known_names = self.__db.get_all_image_names()
            known_encodings = self.__db.get_all_image_encodings()
        except Exception as e:
            print(e)

        # Set start time to calculate the elapsed time
        start = time.time()

        # Read frame by frame
        while True:
            # If the elapsed time has exceeded time_out, stop the loop
            stop = time.time()
            if stop - start > time_out:
                break

            # Capture frame
            ret, frame = video_capture.read()

            # Scale the image to be smaller for easier recognition
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Change the BGR image to RGB image to use face_recognition
            rgb_small_frame = small_frame[:, :, ::-1]

            # Find the location of all faces (known or unknown) in the frame
            # and generate their encodings
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            # For every found face, compare it with all the known face encoding in our database
            matched_name = None
            matched_location = None
            for i in range(len(face_encodings)):
                found_encoding = face_encodings[i]
                matches = face_recognition.compare_faces(known_encodings, found_encoding, tolerance=0.4)
                # If there is a match, we added the name of the recognised face in an araray
                if True in matches:
                    matched_location = face_locations[i]
                    matched_name = FaceDetector.get_target_name(known_names[matches.index(True)])

            # We draw an rectangular box around the recognised face
            if matched_name is not None:
                # Get the location of the matched face
                top, right, bottom, left = matched_location

                # Calculate the location of the bigger image based on the scale down image
                # ie 4 times bigger than the scale down version
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                # We also add a name to our frame for better UI
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, matched_name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display that frame
            cv2.imshow("Image", frame)

            # If user presses the stop key, we will stop immediately
            if cv2.waitKey(1) & 0xFF == ord(stop_key):
                break

            # If any face is found, return the name of the matched face
            if matched_name is not None:
                time.sleep(3)
                video_capture.release()
                cv2.destroyAllWindows()
                return matched_name

        # Otherwise we return None
        video_capture.release()
        cv2.destroyAllWindows()
        return None


if __name__ == '__main__':
    detect = FaceDetector(config["dataset"])
    print(detect.detect())
