from Authentication import Authentication
from FaceRecognition.face_register import FaceRegisterer
from FaceRecognition.face_detector import FaceDetector
from Connection.client import Client
from config import config
import os


class Menu:
    def __init__(self):
        self.__auth = Authentication(config["local_database"])
        self.__messenger = Client(config["udp_client_port"], config["udp_server_port"])
        self.__face_detector = FaceDetector(config["dataset"])
        self.__face_registerer = FaceRegisterer(config["dataset"])

    @staticmethod
    def separate():
        print("*"*102)

    def listen_for_logged_out(self):
        print("Waiting for log out...")
        resp = self.__messenger.read_response().decode()
        if resp == "logout":
            print("Logged out")
            os.system('clear')

    def display_menu(self):
        os.system('clear')
        while True:
            Menu.separate()
            option1 = "1. Create new user (via username and password)"
            option2 = "2. Create new user (via facial recognition)"
            option3 = "3. Login (via username and password)"
            option4 = "4. Login (via facial recognition)"
            print("{}\n{}\n{}\n{}\n".format(option1, option2, option3, option4))
            choice = input("Choose an option: ")

            if choice == "1":
                name = input("Enter username: ")
                pwd = input("Enter a password: ")
                try:
                    self.__auth.save(name, pwd)
                except Authentication.UserExistsException:
                    print("This user already exists")
                except Authentication.PasswordNotValid as e:
                    print("Password not valid: \n{}".format(e))
                except Exception as e:
                    print("Error encountered: {}".format(e))
            elif choice == "2":
                try:
                    name = input("Enter your name: ")
                    self.__face_registerer.capture(name=name, stop_key='q')
                    print("Your details have been captured.")
                except Exception as e:
                    print(e)
            elif choice == "3":
                name = input("Enter username: ")
                pwd = input("Enter password: ")
                try:
                    if self.__auth.check_valid(name, pwd):
                        print("Access granted")
                        try:
                            self.__messenger.send_message(message=name)
                            # Wait for message
                            self.listen_for_logged_out()
                        except Exception as e:
                            print(e)
                    else:
                        print("Invalid credentials. Please try again...")
                except Exception as e:
                    print("Error encountered: {}".format(e))
            elif choice == "4":
                detected_name = self.__face_detector.detect()
                if detected_name is not None:
                    print("Access granted")
                    self.__messenger.send_message(message=detected_name)
                    # Wait for message
                    self.listen_for_logged_out()
                else:
                    print("Not recognised")
            else:
                print("Invalid choice. Try again.")


if __name__ == '__main__':
    menu = Menu()
    menu.display_menu()
