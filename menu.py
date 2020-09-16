from MP.car_database import CarDatabase
from MP.rented_car import RentedCarDB
from MP.car_db import CarDB
from SpeechRecognition import SpeechRecognition
import os
from config import config


'''
This class represents a convenient menu in which users can undertake tasks such as search, view or borrow and return 
cars
'''


class Menu:
    # This menu will receive a username as a parameter for each login
    # This username will be used to identify users when borrowing or returning cars
    def __init__(self, name):
        self.__username = name
        self.__car_db = CarDatabase.from_config(config)
        self.__user = None

    @staticmethod
    def cls():
        os.system('cls' if os.name == 'nt' else 'clear')

    # Print a line of star (separator) to make our options clearer
    @staticmethod
    def separate():
        print("*"*102)

    # We save the user to the cloud database if not already exists
    def init(self):
        self.__car_db.register_MP_user(self.__username)
        self.__user = self.__car_db.getUser(self.__username)

    def display_menu(self):
        option1 = "Search car catalogue."
        option2 = "Borrow a car/cars"
        option3 = "Return a car/cars"
        option4 = "Logout"
        while True:
            Menu.separate()
            print("1: " + option1)
            print("2: " + option2)
            print("3: " + option3)
            print("4: " + option4)
            userInput = input("Enter you choice: ")

            if userInput == "1":
                print("You have selected " + option1)
                while True:
                    carSearchOption = input("What would you like to search by?\n1.Brand\n2.Seats\n3.Body Type\n"
                                               "4.Cost Per Hour\nYour choice: ")
                    if carSearchOption == "1":
                        brand = input("Enter brand:")

                        result = self.__car_db.searchByBrand(brand)
                        if result:
                            CarDatabase.displayInfo([result])
                        else:
                            print("The car with id {} does not exist".format(result))
                    elif carSearchOption == "2":
                        seats = input("Enter the seats:")

                        results = self.__car_db.searchByNoSeats(seats)
                        CarDatabase.displayInfo(results)
                    elif carSearchOption == "3":
                        bodyType = input("Enter body:")

                        results = self.__car_db.searchByBodyType(bodyType)
                        CarDatabase.displayInfo(results)
                    elif carSearchOption == "4":
                        costPerHour = input("Enter car's cost per hour:")

                        results = self.__car_db.searchByCost(costPerHour)
                        CarDatabase.displayInfo(results)
                    elif carSearchOption == "5":
                        break
                    else:
                        print("Invalid input. Please try again")

            elif userInput == "2":
                print("You have selected " + option2)
                carId = input("Enter car id: ")
                try:
                    self.__car_db.rentedCar(self.__user["id"], carId)
                except CarDB.CarDoesNotExists:
                    print("This car does not exist")
                except RentedCarDB.CarRented:
                    print("Car already rented")
                except Exception as e:
                    print(e)
                else:
                    print("Car is rented successfully")

            elif userInput == "3":
                print("You have selected " + option3)
                carId = input("Enter car id: ")
                try:
                    self.__car_db.returnCar(self.__user["id"], carId)
                except RentedCarDB.CarNotRented:
                    print("Car is not rented")
                else:
                    print("Car is returned successfully")

            elif userInput == "4":
                print("You have selected " + option4)
                Menu.cls()
                break
            else:
                print("Wrong entry, enter again.")


if __name__ == "__main__":
    menu = Menu("CarRented")
    menu.init()
    menu.display_menu()
