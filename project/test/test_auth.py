import unittest
from project import main

class TestAuth(unittest.TestCase):

    def test_validateEmail(self):
        self.assertTrue(main.validateEmail("test@test.com"))
        self.assertFalse(main.validateEmail("test@test.c"))
        self.assertFalse(main.validateEmail("@test.com"))
        self.assertFalse(main.validateEmail("testtest.com"))
        self.assertFalse(main.validateEmail("test@testcom"))

    def test_validatePassword(self):
        self.assertTrue(main.validatePassword("Password1"))
        self.assertFalse(main.validatePassword("password1"))
        self.assertFalse(main.validatePassword("Pass1"))
        self.assertFalse(main.validatePassword("PasswordPasswordPasswordPassword1"))
        self.assertFalse(main.validatePassword("PasswordPassword"))

    def test_validateTel(self):
        self.assertTrue(main.validateTel("07000 123456"))
        self.assertTrue(main.validateTel("07000123456"))
        self.assertFalse(main.validateTel("07000 12345"))
        self.assertFalse(main.validateTel("17000 123456"))

    def test_matchPassword(self):
        self.assertTrue(main.matchPasswords("Password1", "Password1"))
        self.assertFalse(main.matchPasswords("Password1", "Password2"))



if __name__ == '__main__':
    unittest.main()