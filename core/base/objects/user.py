from dataclasses import dataclass
from typing import List

from engine.data_persistence import load_data, save_data
from engine.character_registry import class_registry
import core.base.objects.actors.player as pa
import core.base.objects.character as char


@dataclass
class User:
    username: str
    socket_id: str = "sid123"
    is_ready: bool = False
    characters: List['char.Character'] or None = None
    chosen_character: 'char.Character' or None = None
    player_actor: 'pa.PlayerActor' = None

    def __post_init__(self):
        self.characters: List['char.Character'] = []
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
                return f"You have chosen {c.character_name}"
            else:
                self.chosen_character = None

        return "You do not have a character with that name"

    def map_to_savable_dict(self):
        savable_dict = {
            "username": self.username,
            "characters": []
        }

        for character in self.characters:
            savable_dict["characters"].append(character.map_to_savable_dict())

        return savable_dict
