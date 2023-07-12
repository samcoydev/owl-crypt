import json
import os

from engine.constants import SAVE_FILES_PATH


def save_data(file_name, data):
    data_path = os.path.join(SAVE_FILES_PATH, file_name + ".json")

    with open(data_path, "w") as f:
        json.dump(data, f)


def load_data(file_name) -> dict:
    data_path = os.path.join(SAVE_FILES_PATH, file_name + ".json")

    if not os.path.exists(data_path):
        return {}

    with open(data_path, "r") as f:
        data_dict = json.load(f)

    return data_dict


def clear_data_file(file_name):
    data_path = os.path.join(SAVE_FILES_PATH, file_name + ".json")

    if not os.path.exists(data_path):
        return

    with open(data_path, "w") as f:
        json.dump({}, f)
        f.close()
