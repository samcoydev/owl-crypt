# import json
# import os
# import pytest
#
# from core.engine.data_persistence import load_data
# from core.base.objects.user import User
# from core.engine.engine import Engine
#
# @pytest.fixture
# def setup(tmp_path):
#     data_dir = tmp_path / "save_data"
#     data_dir.mkdir()  # Create the 'save_data' directory
#
#     # Use an absolute path for the data file
#     data_path = data_dir / "my_cool_username.json"
#     with open(data_path, "w") as f:
#         json.dump({}, f)
#
#     user = User("my_cool_username", "1111")
#     user.save_user()
#
#     return user, data_path
#
# def test_load_user_save_data(setup):
#     user, data_path = setup
#
#     loaded_data = load_data(user.username)
#     assert loaded_data == user.map_to_savable_dict()
#
#     # User creates a Character
#     user.create_new_character("John the Mighty!", "paladin")
#
#     loaded_data = load_data(user.username)
#     assert loaded_data == user.map_to_savable_dict()