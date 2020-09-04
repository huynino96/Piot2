import mysql.connector
from config import config

'''
This class is for interacting with the car table in our database
'''


class CarDB:
    class CarDoesNotExists(Exception):
        pass

    def __init__(self, config):
        # Config object holds the information of our MySQL connection
        self.__db = mysql.connector.connect(
            host=config["host"],
            user=config["user"],
            passwd=config["password"],
            database=config["database"]
        )

    def close(self):
        if self.__db:
            self.__db.close()

    def getAllCars(self):
        cursor = self.__db.cursor()
        cursor.execute("SELECT carId, plateNumber, make, bodyType, color, seats, location, costPerHour FROM car")
        cars = cursor.fetchall()
        # Converting the tuples returned by cursor.fetchall() into dictionary for more meaningful calls
        return [{
            "id": item[0],
            "plateNumber": item[1],
            "make": item[2],
            "bpdyType": item[3],
            "color": item[4],
            "seats": item[5],
            "location": item[6],
            "costPerHour": item[7]
        } for item in cars] if cars is not None else []

    def addNewCook(self, plateNumber, make, bodyType, color, seats, location, costPerHour):
        cursor = self.__db.cursor()
        cursor.execute("INSERT INTO car (plateNumber, make, bodyType, color, seats, location, costPerHour) VALUES(%s, %s, %s)",
                       (plateNumber, make, bodyType, color, seats, location, costPerHour))
        self.__db.commit()

    # This method will find every car whose name is like the parameter we provided
    # Search car by their Brand
    def searchByMake(self, make):
        cursor = self.__db.cursor()
        cursor.execute("SELECT carId, plateNumber, make, bodyType, color, seats, location, costPerHour FROM car"
                       " WHERE LOWER(make) LIKE %s", ("%" + make + "%",))
        cars = cursor.fetchall()
        return [
            {
                "id": car[0],
                "plateNumber": car[1],
                "make": car[2],
                "bpdyType": car[3],
                "color": car[4],
                "seats": car[5],
                "location": car[6],
                "costPerHour": car[7]
            } for car in cars
        ] if cars is not None else []
    
    def searchByPlateNumber(self, plateNumber):
        cursor = self.__db.cursor()
        cursor.execute("SELECT carId, plateNumber, make, bodyType, color, seats, location, costPerHour FROM car"
                       " WHERE plateNumber) LIKE %s", ("%" + plateNumber + "%",))
        cars = cursor.fetchall()
        return [
            {
                "id": car[0],
                "plateNumber": car[1],
                "make": car[2],
                "bpdyType": car[3],
                "color": car[4],
                "seats": car[5],
                "location": car[6],
                "costPerHour": car[7]
            } for car in cars
        ] if cars is not None else []

    # The same as above, but for body type like SUV, Sedan,...
    def searchByBodyType(self, bodyType):
        cursor = self.__db.cursor()
        cursor.execute("SELECT carId, plateNumber, make, bodyType, color, seats, location, costPerHour FROM car"
                       " WHERE bodyType LIKE %s", ("%" + bodyType + "%",))
        cars = cursor.fetchall()
        return [
            {
                "id": car[0],
                "plateNumber": car[1],
                "make": car[2],
                "bpdyType": car[3],
                "color": car[4],
                "seats": car[5],
                "location": car[6],
                "costPerHour": car[7]
            } for car in cars
        ] if cars is not None else []

    # Search for number of seats
    def searchByNumSeats(self, seats):
        cursor = self.__db.cursor()
        cursor.execute("SELECT carId, plateNumber, make, bodyType, color, seats, location, costPerHour FROM car"
                       " WHERE seats LIKE %s", ("%" + seats + "%",))
        cars = cursor.fetchall()
        return [
            {
                "id": car[0],
                "plateNumber": car[1],
                "make": car[2],
                "bpdyType": car[3],
                "color": car[4],
                "seats": car[5],
                "location": car[6],
                "costPerHour": car[7]
            } for car in cars
        ] if cars is not None else []
    
    # Cost per Hour
    def searchByCost(self, costPerHour):
        cursor = self.__db.cursor()
        cursor.execute("SELECT carId, plateNumber, make, bodyType, color, seats, location, costPerHour FROM car"
                       " WHERE costPerHour LIKE %s", ("%" + costPerHour + "%",))
        cars = cursor.fetchall()
        return [
            {
                "id": car[0],
                "plateNumber": car[1],
                "make": car[2],
                "bpdyType": car[3],
                "color": car[4],
                "seats": car[5],
                "location": car[6],
                "costPerHour": car[7]
            } for car in cars
        ] if cars is not None else []

    # Search for location
    def searchByLocation(self, location):
        cursor = self.__db.cursor()
        cursor.execute("SELECT carId, plateNumber, make, bodyType, color, seats, location, costPerHour FROM car"
                       " WHERE location LIKE %s", ("%" + location + "%",))
        cars = cursor.fetchall()
        return [
            {
                "id": car[0],
                "plateNumber": car[1],
                "make": car[2],
                "bodyType": car[3],
                "color": car[4],
                "seats": car[5],
                "location": car[6],
                "costPerHour": car[7]
            } for car in cars
        ] if cars is not None else []

    # This method is somewhat special, as it will not return an array like the ones above
    # It will return a car dictionary if id exists, otherwise a None
    def getCar(self, carId):
        cursor = self.__db.cursor()
        cursor.execute("SELECT carId, plateNumber, make, bodyType, color, seats, location, costPerHour FROM car WHERE carId = %s",
                       (carId,))
        car = cursor.fetchone()
        return {
                "id": car[0],
                "plateNumber": car[1],
                "make": car[2],
                "bpdyType": car[3],
                "color": car[4],
                "seats": car[5],
                "location": car[6],
                "costPerHour": car[7]
        } if car is not None else None


if __name__ == '__main__':
    db = CarDB(config)
    print(db.searchByMake("Mercedes Benz"))
