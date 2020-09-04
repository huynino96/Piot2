import mysql.connector

'''
This class is for interacting with our event table, which holds the event string of the Google Calender Event
In order to delete (remove) an event, the event string will be retrieved using this class
It is worth noting that for every rented car record, there is one and only one matching event string
'''


class EventDB:
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

    def saveEvent(self, rentedId, eventString):
        cursor = self.__db.cursor()
        cursor.execute("INSERT INTO event(rentedId, eventString) VALUES (%s, %s)", (rentedId, eventString))
        self.__db.commit()

    # Remove the event using the rented id to retrieve the event string id saved
    def removeEvent(self, rentedId):
        cursor = self.__db.cursor()
        cursor.execute("DELETE FROM event WHERE rentedId = %s", (rentedId,))
        self.__db.commit()

    # Get event string of a rented car instance
    def getEventString(self, rentedId):
        cursor = self.__db.cursor()
        cursor.execute("SELECT eventString FROM event WHERE rentedId = %s", (rentedId,))
        instance = cursor.fetchone()
        return instance[0] if instance is not None else None

