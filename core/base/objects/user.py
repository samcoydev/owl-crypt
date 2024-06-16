from typing import List

from core.engine.data_persistence import load_data, save_data
from core.engine.character_registry import class_registry
import core.base.objects.character as char


class User:
    def __init__(self, username, pin, socket_id="sid123", is_ready=False):
        self.username = username
        self.pin = pin
        self.socket_id = socket_id
        self.is_ready = is_ready
        self.characters: List['char.Character'] = []
        self.chosen_character = None
        self.player_actor = None
        self.load_user_save_data()

    def load_user_save_data(self):
        data_dict = load_data(self.username)

        if len(data_dict) > 0:
            for character_data in data_dict["characters"]:
                c: 'char.Character' = class_registry[character_data["class_name"]]("")
                c.load_saved_data(character_data)
                self.characters.append(c)

    def save_user(self):
        save_data(self.username, self.map_to_savable_dict())

    def create_new_character(self, character_name: str, character_class_name: str):
        new_character: 'char.Character' = class_registry[character_class_name](character_name)

        # Add new character to user's character sheet
        self.characters.append(new_character)
        self.save_user()

    def pick_character(self, character_name: str):
        """When a User calls PICK <character_name>"""
        for c in self.characters:
            if c.character_name == character_name:
                self.chosen_character = c
                if c.stats_dicts is None:
                    c.stats_dicts = char.get_base_stats()
                return f"You have chosen {c.character_name}"
            else:
                self.chosen_character = None

        return "You do not have a character with that name"

    def map_to_savable_dict(self):
        savable_dict = {
            "username": self.username,
            "pin": self.pin,
            "characters": []
        }

        for character in self.characters:
            savable_dict["characters"].append(character.map_to_savable_dict())

        return savable_dict

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return self.is_active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def __str__(self):
        return "User: " + self.username + " with PIN: " + self.pin + " and socket_id: " + self.socket_id + " is ready: " + str(self.is_ready) + " with characters: " + str(self.characters) + " and chosen character: " + str(self.chosen_character) + " and player actor: " + str(self.player_actor)
