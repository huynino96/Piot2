import datetime
import mysql.connector

'''
This class is for interacting with the rented car table in the database
'''


class RentedCarDB:
    class CarRented(Exception):
        pass

    class CarNotRented(Exception):
        pass

    # Return a return day for a car, which is by default 7 days after the borrow day
    @staticmethod
    def getReturnDate(rentedDate, allowedDays=7):
        return rentedDate + datetime.timedelta(days=allowedDays)

    # Formatting a datetime object to be inserted to our database
    @staticmethod
    def formatDate(date):
        return date.strftime("%Y-%m-%d %H:%M:%S")

    def __init__(self, config):
        self.__db = mysql.connector.connect(
            host=config["host"],
            user=config["user"],
            passwd=config["password"],
            database=config["database"]
        )

    def close(self):
        if self.__db:
            self.__db.close()

    # Check if a car with a specific id is rented
    def ifCarIsrented(self, carId):
        cursor = self.__db.cursor()
        cursor.execute("SELECT status FROM rentedCar WHERE carId = %s ORDER BY rentedDate DESC",
                       (carId,))
        allRented = cursor.fetchall()    # Using fetchall to make sure that cursor will not raise an error
        rented = allRented[0] if allRented and len(allRented) > 0 else None
        if rented is None or rented[0] == 'returned':
            return False
        return True

    # Get a record (in the form of a dictionary) in the table
    def getRented(self, rentedId):
        cursor = self.__db.cursor()
        cursor.execute("SELECT rentedId, userId, carId, rentedDate, returnedDate, status FROM rentedCar "
                       "WHERE rentedId = %s", (rentedId,))
        allRented = cursor.fetchall()    # Using fetchall to make sure that cursor will not raise an error
        rented = allRented[0] if allRented and len(allRented) > 0 else None
        return {
            "id": rented[0],
            "userId": rented[1],
            "carId": rented[2],
            "rentedDate": rented[3],
            "returnedDate": rented[4],
            "status": rented[5]
        } if rented is not None else None

    # Borrow a car by inserting a record to the table
    def rentCar(self, userId, carId):
        # Check if car is rented
        if self.ifCarIsrented(carId):
            raise RentedCarDB.CarRented()

        # Get borrow date - Which is now
        borrowDate = datetime.datetime.now()

        # Add to rented car lib
        cursor = self.__db.cursor()
        cursor.execute("INSERT INTO rentedCar (carId, userId, status, rentedDate)"
                       " VALUES (%s, %s, %s, %s)", (carId, userId, 'rented',
                                                    RentedCarDB.formatDate(borrowDate)))
        self.__db.commit()

        # Return the id for this newest rentedId
        return cursor.lastrowid

    # Return a car by update the record we have created in the above method
    def returnCar(self, userId, carId):
        # Get the rented car instance
        cursor = self.__db.cursor()
        cursor.execute("SELECT rentedId FROM rentedCar WHERE userId = %s AND carId = %s AND status = %s",
                       (userId, carId, 'rented'))
        rented = cursor.fetchone()

        # Check if exists
        if not rented:
            raise RentedCarDB.CarNotRented()
        else:
            # Get returned date
            returnedDate = datetime.datetime.now()
            rentedId = rented[0]

            #  Update instance
            cursor.execute("UPDATE rentedCar SET status = %s, returnedDate = %s WHERE rentedId = %s",
                           ('returned', RentedCarDB.formatDate(returnedDate), rentedId))
            self.__db.commit()

            # Return the return car id
            return rentedId
