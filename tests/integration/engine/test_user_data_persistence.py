import json
import os
import unittest

from engine.database.database_manager import load_data
from engine.objects.user import User


class UserDataPersistence(unittest.TestCase):

    def setUp(self) -> None:
        self.data_dir = os.path.join(os.getcwd(), "save_data")
        os.makedirs(self.data_dir, exist_ok=True)  # Create the 'save_data' directory if it doesn't exist

        # Use an absolute path for the data file
        self.data_path = os.path.join(self.data_dir, "my_cool_username.json")
        with open(self.data_path, "w") as f:
            json.dump({}, f)
            f.close()

    def tearDown(self):
        os.remove(self.data_path)

    def test_load_user_save_data(self):
        # User joins for the first time and creates a user object in the engine
        self.user = User("my_cool_username")
        self.user.save_user()

        self.loaded_data = load_data(self.user.username)
        self.assertEqual(self.loaded_data, self.user.map_to_savable_dict())

        # User creates a Character
        self.user.create_new_character("John the Mighty!", "paladin")

        self.loaded_data = load_data(self.user.username)
        self.assertEqual(self.loaded_data, self.user.map_to_savable_dict())
