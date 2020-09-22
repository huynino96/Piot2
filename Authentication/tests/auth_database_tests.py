import unittest
from Authentication import Authentication
import mock


class TestAuthentication(unittest.TestCase):
    @mock.patch('Authentication.auth_database.AuthDatabase', autospec=True)
    def test_save(self, auth_database_constr):
        pass

    def test_clean_up(self):
        pass

    def test_check_valid(self):
        pass


if __name__ == '__main__':
    unittest.main()