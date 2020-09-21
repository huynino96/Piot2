import mysql.connector


'''
This class is for interacting with the user table in our database
'''


class UserDB:
    class UserExistException(Exception):
        pass

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

    def getAllUsers(self):
        cursor = self.__db.cursor()
        cursor.execute("SELECT userId, userName FROM user")
        users = cursor.fetchall()
        return [
            {
                "id": item[0],
                "firstName": item[1],
                "lastName": item[2],
                "userName": item[3],
                "email": item[4]
            } for item in users
        ] if users is not None else []

    def exists(self, username):
        cursor = self.__db.cursor()
        cursor.execute("SELECT userId FROM user WHERE userName = %s", (username,))
        users = cursor.fetchall()
        return True if users and len(users) > 0 else False

    def getUser(self, username):
        cursor = self.__db.cursor()
        cursor.execute("SELECT userId, firstName, lastName, userName, email FROM user WHERE userName = %s", (username,))
        user = cursor.fetchone()
        return {
            "id": user[0],
            "firstName": user[1],
            "lastName": user[2],
            "userName": user[3],
            "email": user[4],
        } if user is not None else None

    # Save a user if not exists, otherwise raise an exception
    def register(self, username):
        if self.getUser(username) is None:
            cursor = self.__db.cursor()
            cursor.execute("INSERT INTO user (userName) VALUES(%s)", (username,))
            self.__db.commit()
            return cursor.lastrowid
        else:
            raise UserDB.UserExistException()
