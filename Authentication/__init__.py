from Authentication.auth_db import AuthDatabase
from Authentication.hashing import Hasher
from Authentication.validator import Validator


'''
This class is for managing user for our LMS.
Its tasks include registering a user, and checking if login credentials is valid
'''


class Authentication:
    class UserExistsException(Exception):
        pass

    class PasswordNotValid(Exception):
        pass

    def __init__(self, filename):
        self.__db = AuthDatabase(filename)
        self.__db.open()
        self.__db.create_database()

    def save(self, username, plain_text_password):
        # Check for overlapped username
        if self.__db.exists(username):
            raise Authentication.UserExistsException()

        # Validate password before persists into the database
        messages = Validator.getMessage(plain_text_password)
        if len(messages) > 0:
            raise Authentication.PasswordNotValid('\n'.join(messages))

        # Hash password and save to database
        hashed_password = Hasher.hash(plain_text_password)
        self.__db.add_user(username, hashed_password)

    def clean_up(self):
        self.__db.close()

    def check_valid(self, username, plain_text_password):
        # Check if username exists in database
        usr_with_same_name = self.__db.get_with_name(username)
        if not usr_with_same_name:
            return False

        # Then check if password is valid
        pwd = usr_with_same_name["password"]
        return Hasher.if_matched(plain_text_password, pwd)


if __name__ == '__main__':
    auth = Authentication("hello.db")
    try:
        if auth.check_valid("John", "Long1234"):
            print("Matched")
    except Exception as e:
        print(e)
    finally:
        auth.clean_up()