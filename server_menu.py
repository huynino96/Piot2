from LMS.menu import Menu as LMSMenu
from config import config
from Connection.server import Server
import os


class Menu:
    def __init__(self):
        self.__receiver = Server(config["udp_server_port"], config["udp_client_port"])
        self.__lms_menu = None

    def on_receive(self, data):
        if data is not None:
            username = data.decode('utf-8')
            print("Connection opened. Please wait for the LMS menu to start...")
            self.display_menu(username)

    def display_menu(self, username):
        os.system('clear')
        self.__lms_menu = LMSMenu(username)
        self.__lms_menu.init()
        self.__lms_menu.display_menu()
        self.__receiver.send_message("logout")

    def start_listening(self):
        print("Waiting for client to connect")
        self.__receiver.listening(self.on_receive)


if __name__ == '__main__':
    menu = Menu()
    menu.start_listening()
