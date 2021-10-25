import unittest
from project import auth

class TestAuth(unittest.TestCase):

    def test_validateEmail(self):
        self.assertTrue(auth.validateEmail("test@test.com"))
        self.assertFalse(auth.validateEmail("test@test.c"))
        self.assertFalse(auth.validateEmail("@test.com"))
        self.assertFalse(auth.validateEmail("testtest.com"))
        self.assertFalse(auth.validateEmail("test@testcom"))

    def test_validatePassword(self):
        self.assertTrue(auth.validatePassword("Password1"))
        self.assertFalse(auth.validatePassword("password1"))
        self.assertFalse(auth.validatePassword("Pass1"))
        self.assertFalse(auth.validatePassword("PasswordPasswordPasswordPassword1"))
        self.assertFalse(auth.validatePassword("PasswordPassword"))

    def test_validateTel(self):
        self.assertTrue(auth.validateTel("07000 123456"))
        self.assertTrue(auth.validateTel("07000123456"))
        self.assertFalse(auth.validateTel("07000 12345"))
        self.assertFalse(auth.validateTel("17000 123456"))

    def test_matchPassword(self):
        self.assertTrue(auth.matchPasswords("Password1", "Password1"))
        self.assertFalse(auth.matchPasswords("Password1", "Password2"))



if __name__ == '__main__':
    unittest.main()