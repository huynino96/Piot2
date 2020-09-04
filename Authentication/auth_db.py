import sqlite3
from config import config

'''
This class is for persist username and hashed password into a local database named 'filename'
'''


class AuthDatabase:
    def __init__(self, filename):
        self.__filename = filename
        self.__conn = None

    def open(self):
        self.__conn = sqlite3.connect(self.__filename)

    def close(self):
        if self.__conn:
            self.__conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # Create a user database if not already created
    def create_database(self):
        cursor = self.__conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users(
            ID integer PRIMARY KEY, 
            NAME VARCHAR(100) NOT NULL, 
            PWD VARCHAR(100) NOT NULL
        )''')

    # Transaction must be committed for changes to take place
    def commit_transaction(self):
        self.__conn.commit()

    def add_user(self, username, hashed_password):
        cursor = self.__conn.cursor()
        cursor.execute("INSERT INTO users VALUES(NULL, ?, ?)", (username, hashed_password))
        self.commit_transaction()

    def get_all_users(self):
        results = []
        cursor = self.__conn.execute("SELECT NAME, PWD FROM users")
        for item in cursor:
            results.append({"name": item[0], "password": item[1]})
        return results

    # Get user with a specific username, return None if not created
    def get_with_name(self, username):
        cursor = self.__conn.execute("SELECT NAME, PWD FROM users WHERE NAME = ?", (username,))
        matched = cursor.fetchone()
        if matched:
            return {"name": matched[0], "password": matched[1]}
        return None

    # Check if user with a specific username exists
    def exists(self, username):
        cursor = self.__conn.execute("SELECT NAME, PWD FROM users WHERE NAME = ?", (username,))
        found = cursor.fetchone()
        return True if found else False


if __name__ == "__main__":
    try:
        with AuthDatabase(config["local_database"]) as db:
            db.open()
            db.create_database()
            for user in db.get_all_users():
                print(user)
    except Exception as e:
        print(e)



