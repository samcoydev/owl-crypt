# import os
# import unittest
#
# from core.engine.data_persistence import save_data, load_data
#
#
# class DataPersistenceManagerTests(unittest.TestCase):
#
#     def helper_get_test_user(self):
#         return {
#             "username": "test_user",
#             "name": "Andrew",
#             "characters": [
#                 {
#                     "character_name": "John the Slayer",
#                     "class_name": "soldier"
#                 }
#             ]
#         }
#
#     @classmethod
#     def tearDownClass(cls):
#         os.remove(os.path.join(os.getcwd(), "save_data", "test_user.json"))
#         os.remove(os.path.join(os.getcwd(), "save_data", "john_user.json"))
#
#     def test_save_data_and_load_data(self):
#         self.data = self.helper_get_test_user()
#         save_data(self.data["username"], self.data)
#
#         self.loaded_data = load_data(self.data["username"])
#         self.assertEqual(self.loaded_data, self.data, "The loaded data does not represent the saved data properly")
#
#     def test_updating_data(self):
#         # Create initial entry
#         self.data = self.helper_get_test_user()
#         self.data["username"] = "john_user"
#         save_data(self.data["username"], self.data)
#
#         # Create Character
#         self.character = {"character_name": "Brigade", "class_name": "paladin"}
#         self.data["characters"].append(self.character)
#         save_data(self.data["username"], self.data)
#
#         self.loaded_data = load_data(self.data["username"])
#         self.assertEqual(self.loaded_data, self.data, "The loaded data does not represent the updated data properly")
