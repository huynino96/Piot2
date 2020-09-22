import unittest
from Authentication.hash import Hasher
import re


class TestHashMethods(unittest.TestCase):
    def setUp(self):
        self.words = ["Hello", "Word", "Man", "NoSon", "The end is near", "Awesome"]

    def test_hash_format(self):
        for word in self.words:
            hash = Hasher.hash(word)
            self.assertEqual(len(hash), 60)
            self.assertTrue(re.match("^\\$2[a-z]\\$12.*$", hash))

    def check_hash_match(self):
        for word in self.words:
            hash = Hasher.hash(word)
            self.assertTrue(Hasher.if_matched(word, hash))


if __name__ == '__main__':
    unittest.main()
