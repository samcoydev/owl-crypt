import json
import os

from engine.database.constants import SAVE_FILES_PATH


def save_data(file_name, data):
    data_path = os.path.join(SAVE_FILES_PATH, file_name + ".json")

    if not os.path.exists(data_path):
        print(f"Save file for {data_path} does not exist. Creating new file.")

    with open(data_path, "w") as f:
        json.dump(data, f)
    print(f"Data written to {data_path} successfully.")


def load_data(file_name) -> dict:
    data_path = os.path.join(SAVE_FILES_PATH, file_name + ".json")

    if not os.path.exists(data_path):
        print(f"Save file for {data_path} does not exist. Please make sure the name is right, and that the init "
              "files method was called correctly.")
        return {}

    with open(data_path, "r") as f:
        data_dict = json.load(f)

    return data_dict


def clear_data_file(file_name):
    data_path = os.path.join(SAVE_FILES_PATH, file_name + ".json")

    if not os.path.exists(data_path):
        print(f"Save file for {data_path} does not exist. Please make sure the name is right, and that the init "
              "files method was called correctly.")
        return

    with open(data_path, "w") as f:
        json.dump({}, f)
        f.close()
