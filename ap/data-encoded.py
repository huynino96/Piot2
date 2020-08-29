import os
import pickle
from imutils import paths
import cv2
import face_recognition


class FaceEncoded():
    """
    Face data encode 
    """

    @staticmethod
    def encode():
        """
        Encode the images into appropriate format
        :return: None
        """
        # grab the paths to the input images in our dataset
        print("[INFO] Quantifying faces...")
        imgPaths = list(paths.list_images("dataset"))

        # initialize the list of known encodings and known names
        encodingList = []
        nameList = []

        # loop over the image paths
        for (i, imgPaths) in enumerate(imgPaths):
            # extract the person name from the image path
            print("[INFO] processing image {}/{}".format(i + 1, len(imgPaths)))
            name = imgPaths.split(os.path.sep)[-2]

            # load the input image and convert it from RGB (OpenCV ordering)
            # to dlib ordering (RGB)
            image = cv2.imread(imgPaths)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input image
            boxes = face_recognition.face_locations(rgb, model="hog")

            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)

            # loop over the encodings
            for encoding in encodings:
                # add each encoding + name to our set of known names and encodings
                encodingList.append(encoding)
                nameList.append(name)

        # dump the facial encodings + names to disk
        print("[INFO] serializing encodings...")
        data = {"encodings": encodingList, "names": nameList}

        with open("encodings.pickle", "wb") as encodedFile:
            encodedFile.write(pickle.dumps(data))