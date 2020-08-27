import os
import cv2


class FaceCapture():
    """
    Provide the interface for face images capture
    """

    @staticmethod
    def faceCapture(userName):
        """
        Create a dataset folder where we stored all the face data in there
        """

        # use name as folder name
        facFolderData = "./dataset/{}".format(userName)

        # Create a new folder for the new name
        if not os.path.exists(facFolderData):
            os.makedirs(facFolderData)

        # Start the camera
        camera = cv2.VideoCapture(0)
        # Set width
        camera.set(3, 640)
        # Set height
        camera.set(4, 480)
        # Get the classifier of 3 million faces that had pre-tranied
        faceDetect = cv2.CascadeClassifier("Face-Classifier.xml")

        img_counter = 1
        # Capture maximum 10 picture
        while img_counter <= 10:
            key = input("Press Q to quit or ENTER to continue: ")
            if key == "Q" or key == "q":
                break

            ret, frame = camera.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceDetect.detectMultiScale(gray, 1.3, 5)

            if len(faces) == 0:
                print("No face detected, please try again")
                continue

            for (x, y, weight, height) in faces:
                cv2.rectangle(frame, (x, y), (x + weight, y + height), (255, 0, 0), 2)
                imgName = "{}/{:04}.jpg".format(facFolderData, imgCounter)
                cv2.imwrite(imgName, frame[y: y + height, x: x + weight])
                print("NO.{} image recorded!".format(imgCounter))
                imgCounter += 1

        # release the camera resource
        camera.release()