import unittest
from project import main
from project import validation as vd


class TestDogs(unittest.TestCase):

    def test_validateName(self):
        self.assertTrue(vd.validateDogName("Scout"))
        self.assertFalse(vd.validateDogName("")) # Short/null
        self.assertFalse(vd.validateDogName("ScoutScoutScoutScoutScout")) # Long

    def test_validateBreed(self):
        self.assertTrue(vd.validateBreedName("Labrador"))
        self.assertFalse(vd.validateBreedName(""))
        self.assertFalse(vd.validateBreedName("A" * 51))

    def test_validateAge(self):
        self.assertTrue(vd.validateAge(10))
        self.assertFalse(vd.validateAge(0))
        self.assertFalse(vd.validateAge(21))

    def test_validateSex(self):
        self.assertTrue(vd.validateSex("M"))
        self.assertTrue(vd.validateSex("F"))
        self.assertFalse(vd.validateSex("A"))
        self.assertFalse(vd.validateSex(None))

    def test_validateLocation(self):
        self.assertTrue(vd.validateLocation("East Sussex"))
        self.assertFalse(vd.validateLocation(""))
        self.assertFalse(vd.validateLocation("A" * 51))
        self.assertFalse(vd.validateLocation(None))


if __name__ == '__main__':
    unittest.main()