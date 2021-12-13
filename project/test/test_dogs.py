import unittest
from project import main

class TestDogs(unittest.TestCase):

    def test_validateName(self):
        self.assertTrue(main.validateDogName("Scout"))
        self.assertFalse(main.validateDogName("")) # Short/null
        self.assertFalse(main.validateDogName("ScoutScoutScoutScoutScout")) # Long

    def test_validateBreed(self):
        self.assertTrue(main.validateBreedName("Labrador"))
        self.assertFalse(main.validateBreedName(""))
        self.assertFalse(main.validateBreedName("A" * 51))

if __name__ == '__main__':
    unittest.main()