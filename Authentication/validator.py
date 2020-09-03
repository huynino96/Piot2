import re

'''
This class is for checking if the password is valid (follow rules to ensure it to be more secure)
'''


class Validator:
    @staticmethod
    def checkLenght(string):
        return len(string) > 6

    @staticmethod
    def containsNumber(string):
        numbers = '0123456789'
        for character in string:
            if character in numbers:
                return True

        return False

    @staticmethod
    def checkSpecialChar(string):
        specials = '!@#$%^&*()-_+={}\"[]|\\:;\'<,>.?/'
        for character in string:
            if character in specials:
                return True

        return False

    @staticmethod
    def checkAlphabetChar(string):
        pattern = re.compile('[a-zA-Z]')
        for character in string:
            if pattern.match(character):
                return True
        return False

    # This method will return an array of rules that the password failed to comply to
    # This array will be empty if the password is valid
    @staticmethod
    def getMessage(string):
        message = []
        if not Validator.checkLenght(string):
            message.append("Password must be 6 character or more")
        if not Validator.containsNumber(string):
            message.append("Password must contain a number")
        if not Validator.checkSpecialChar(string):
            message.append("Password must contain a special character")
        if not Validator.checkAlphabetChar(string):
            message.append("Password must contain a alphabetical character")
        return message


if __name__ == '__main__':
    password = "weAreOne!"
    for msg in Validator.getMessage(password):
        print(msg)