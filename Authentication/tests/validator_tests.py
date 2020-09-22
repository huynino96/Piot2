import unittest
from Authentication.validator import Validator


class TestValidatorMethods(unittest.TestCase):
    def setUp(self):
        self.valid_passwords = ["Rm!tt123123", "TheNam3i3Jon!", "TheHe3eatofGol9!", "EndGam3!!T"]
        self.invalid_passwords = ["1122", "J", "Manwrwrwr", "!!!!!!!!", "Phat135797", "12121@@!!"]

    def test_valid_password(self):
        for pwd in self.valid_passwords:
            messages = Validator.get_messages(pwd)
            self.assertEqual(len(messages), 0)

    def test_invalid_password(self):
        for pwd in self.invalid_passwords:
            messages = Validator.get_messages(pwd)
            self.assertGreater(len(messages), 0)

    def test_length(self):
        pwds = ["", "1", "2", "3"]
        for pwd in pwds:
            self.assertFalse(Validator.is_length_ok(pwd))

    def test_number(self):
        pwds = ["sadada", "asdsadad!!!da", "asdf#@!afsaf"]
        for pwd in pwds:
            self.assertFalse(Validator.contains_number(pwd))

    def test_special_characters(self):
        pwds = ["sadada123", "asdsadadda1233213", "aasas", "123123"]
        for pwd in pwds:
            self.assertFalse(Validator.contains_special_character(pwd))

    def test_alphabetical_characters(self):
        pwds = ["!@##@123", "1233213", "^&**&^", "123123^&^^"]
        for pwd in pwds:
            self.assertFalse(Validator.contains_alphabetical_character(pwd))


if __name__ == '__main__':
    unittest.main()
