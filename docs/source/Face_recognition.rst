Face recogniton
===================


Face Register
----------------------------------

* Method: if_face_detected(frame)
    Params: frame: image which can come from a camera
    Function: Return the location of the detected face.

* Method: capture(self, name="Unknown", time_out=10, stop_key='e')
    Params: name, time and stop key can be alter
    Function: If face is detected at the current frame, save the face into face database

Face Detector
----------------------------------

* Static Method: get_target_name(file_path)
    Function: reduce the path of the image to the image name itself

* Method: detect(self, time_out=10, stop_key='q')
    Params: time_out: time detecting face, stop_key: key to press to stop running
    Function: While in recording time, detect face and compare it to the database. If any matches, draw a box around the
        face and display the name of the face.

Face Database
----------------------------------

* Static Method: change_to_gray(frame)
    Params: frame: image
    Function: convert the input frame to gray image and return it.

* Method: get_all_image_names(self)
    Function: return all image name available in database

* Method: get_all_images(self)
    Function: return all image available in database

* Method: get_all_image_encodings(self)
    Function: return all encoded image

* Method: save(self, image, name):
    Param: image: image input, name: face name
    Function: convert the image into gray and save the image with the face name.

Dataset
----------------------------------
Create Dataset folder to save all the face image
