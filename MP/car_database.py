from MP.rented_car import RentedCarDB
from MP.car_db import CarDB
from MP.user_db import UserDB
from MP.event_db import EventDB
from MP.google_api import Calendar
from config import config


'''
This class is a composition of the user_db, car_db, event_db and rented_car_db we created
It will use these classes to simulate an interconnecting system for car management
'''


class carDatabase:
    @staticmethod
    def from_config(config):
        return carDatabase(config)

    def __init__(self, config):
        self.__car_db = CarDB(config)
        self.__rented_db = RentedCarDB(config)
        self.__user_db = UserDB(config)
        self.__event_db = EventDB(config)
        self.__calendar = Calendar(config["client_secrets"])

    def close(self):
        self.__rented_db.close()
        self.__user_db.close()
        self.__car_db.close()
        self.__event_db.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def searchByBrand(self, make):
        return self.__car_db.searchByMake(make)

    def searchByPlateNumber(self, plateNumber):
        return self.__car_db.searchByPlateNumber(plateNumber)

    def searchByBodyType(self, bodyType):
        return self.__car_db.searchByBodyType(bodyType)

    def searchById(self, id):
        return self.__car_db.getCar(id)

    def searchByNoSeats(self, seats):
        return self.__car_db.searchByNumSeats(seats)
    
    def searchByLocation(self, location):
        return self.__car_db.searchByLocation(location)

    def searchByCost(self, costPerHour):
        return self.__car_db.searchByCost(costPerHour)

    def register_MP_user(self, name):
        if not self.__user_db.exists(name):
            self.__user_db.register(name)

    def getUser(self, name):
        return self.__user_db.getUser(name)

    # This method will create a neatly placed frame to display all the information of a car array
    # (an array containing car dictionary)
    @staticmethod
    def displayInfo(cars):
        print("*" * 127)
        print("*{:<25}{:<25s}{:<25s}{:<25s}{:<25s}{:<25s}{:<25s}{:<25s}*".format("CarId", "PlateNumber", "Make", "BodyType", "Color", "Seats", "Location", "CostPerHour"))
        for car in cars:
            print("*{:<25}{:<25s}{:<25s}{:<25s}{:<25s}{:<25s}{:<25s}{:<25s}*".format(car["carId"],
                                                                car["plateNumber"],
                                                                car["make"],
                                                                car["bodyType"],
                                                                car["color"],
                                                                car["seats"],
                                                                car["location"],
                                                                car['costPerHour']))
        print("*" * 127)

        if len(cars) == 0:
            print("404: Car doesn't exist. Please try again")

    def getAllCars(self):
        return self.__car_db.getAllCars()

    def rentedCar(self, userId, carId):
        # car is not in database -> Throw exception
        carInstance = self.searchById(carId)
        if carInstance is None:
            raise CarDB.CarDoesNotExists()

        # Using rented car class to add a record
        rentedId = self.__rented_db.rentCar(userId, carId)
        rented = self.__rented_db.getRented(rentedId)

        # Get date of return
        rentedDate = rented["rentedDate"]

        # Init calendar if not initiated
        if not self.__calendar.if_initiated():
            self.__calendar.init()

        # Add event to Google Calendar
        event = self.__calendar.add_event("car return", "Return {}".format(carInstance["title"]),
                                          RentedCarDB.getReturnDate(rentedDate))

        # Save event string to table for latter removal
        self.__event_db.save_event(rented_id=rentedId, event_string=event["id"])

    def returnCar(self, userId, carId):
        # Return the car using rented car class
        rentedId = self.__rented_db.returnCar(userId, carId)

        # Init calendar if not initiated
        if not self.__calendar.if_initiated():
            self.__calendar.init()

        # Get event string from db
        eventStringId = self.__event_db.get_event_string(rentedId)

        # Remove from calendar using this unique event string id
        self.__calendar.remove_event(eventStringId)
        return rentedId

    # Method to find a car using plate number and return it
    def returnCarByPlateNum(self, userId, plateNumber):
        # Get car
        cars = self.__car_db.searchByPlateNumber(plateNumber)
        if len(cars) == 0:
            raise CarDB.CarDoesNotExists()

        # Get car id (find the first car with the same isbn)
        id = cars[0]["id"]

        # Return
        self.returnCar(userId, id)

    # Method to find a car using name and return it
    # def return_car_using_name(self, user_id, name):
    #     # We will get the first car with matching name from an array of matched cars
    #     cars = self.__car_db.search_by_name(name)
    #     if len(cars) == 0:
    #         raise CarDB.CarDoesNotExists()

        # Get id of the first match
        id = cars[0]["id"]

        # Return a car using the method defined above
        self.returnCar(userId, id)
        return cars[0]["title"]


if __name__ == "__main__":
    with carDatabase.from_config(config) as MP:
        print(MP.searchByPlateNumber('66S-6666'))
