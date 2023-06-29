from abc import ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import engine.objects.actors.player as player_actor


@dataclass
class Character(ABC):
    """
    Represents a characters statistics and handles data persistence. Think of this class as the players D&D Character
    sheet. This class is also the base class for other Character Types, like Paladins or Rogues.
    """
    character_name: str
    _class_name: str
    _special_effects = {}
    signature_command_name: str
    signature_max: int

    current_player_actor: 'player_actor.PlayerActor' or None = None
    _hp: int = 1

    def run_command(self, command_name, args):
        # Check if the command has a special effect for this character class
        if command_name in self._special_effects:
            special_effect = self._special_effects[command_name]
            special_effect(command_name, args)
        else:
            command = self.current_player_actor.game_engine.command_registry[command_name.lower()]
            command.execute(self, args)

    def set_health(self, hp: int) -> None:
        self._hp = hp

    def load_saved_data(self, data: dict):
        """Load a Character"""
        self.character_name = data["name"]
        self._hp = data["health_points"]

    def map_to_savable_dict(self):
        return {
            "name": self.character_name,
            "class_name": self._class_name,
            "health_points": self._hp
        }
