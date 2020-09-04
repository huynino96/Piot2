import cv2
import face_recognition
import os
from config import config

'''
This class is used to retrieve the face dataset to identify known faces
'''


class FaceDatabase:
    def __init__(self, dirname):
        self.__dirname = dirname
        self.__names = None
        self.__images = None
        self.__encodings = None

    # We have to convert image to gray so that it will be easier for the raspberry to handle
    # Using colored images may crash our Pi
    @staticmethod
    def change_to_gray(frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # This method will read all the images file name in our
    # dataset folder, specified by self.__dirname
    # The valid names end with .png and .jpg extensions
    def get_all_image_names(self):
        # Use lazy loading to avoid loading the names too many times
        if not self.__names:
            names = []
            for filename in os.listdir(self.__dirname):
                if filename.endswith(".png") or filename.endswith(".jpg"):
                    names.append(os.path.join(self.__dirname, filename))
            self.__names = names
        return self.__names

    # From the images name, we use face_recognition modules to load all known faces
    def get_all_images(self):
        # Use lazy loading to avoid loading the faces too many times
        if not self.__images:
            all_image_names = self.get_all_image_names()
            self.__images = [face_recognition.load_image_file(img) for img in all_image_names]
        return self.__images

    # From the images returned by face_recognition, we generate encodings for recognition
    # using the function provided by face_recognition
    def get_all_image_encodings(self):
        # Use lazy loading to avoid generating encodings again and again
        if not self.__encodings:
            images = self.get_all_images()
            result = []
            for image in images:
                encodings = face_recognition.face_encodings(image)
                # Only append to results if there is at least an encoding generated
                if len(encodings) > 0:
                    result.append(encodings[0])
            self.__encodings = result
        return self.__encodings

    # We convert the image to gray and then save to our dataset
    def save(self, image, name):
        image = FaceDatabase.change_to_gray(image)
        cv2.imwrite(os.path.join(self.__dirname, name) + ".png", image)


if __name__ == '__main__':
    db = FaceDatabase(config["dataset"])
    for encoding in db.get_all_image_names():
        print(encoding)


