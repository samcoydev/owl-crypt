from abc import ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING
from core.engine.command_registry import command_registry

if TYPE_CHECKING:
    import core.base.objects.actors.player as player_actor

_BASE_STATS = {
    "level": 1,
    "health_points": 1,
    "spell_points": 1,
    "rigidity_points": 1,
    "weight_limit": 1,
    "base_attack_damage": 1,
    "base_magic_damage": 1,
    "stat_points": 0,
    "exp_gained": 0
}


def get_base_stats():
    return _BASE_STATS.copy()


@dataclass
class Character(ABC):
    """
    Represents a characters statistics and handles data persistence. Think of this class as the players D&D Character
    sheet. This class is also the base class for other Character Types, like Paladins or Rogues.
    
    Would not recommend modifying at this time.
    """
    character_name: str
    class_name: str
    signature_command_name: str
    signature_max: int
    _command_weight_overrides = {}  # command_name - energy_cost
    signature_should_override_original_command = False
    should_append_signature_message = False  # Should the signature message appear after the original command text?

    current_player_actor: 'player_actor.PlayerActor' or None = None
    stats_dicts: dict = None

    def level_up(self):
        # Add session gained exp to the characters total gained exp
        self.stats_dicts["exp_gained"] += self.current_player_actor.session_exp_gained
        self.current_player_actor.session_exp_gained = 0

        required_exp_for_next_level = int((50 * self.stats_dicts["level"] + 1) ^ 1.2)
        if self.stats_dicts["exp_gained"] >= required_exp_for_next_level:
            self.stats_dicts["exp_gained"] -= required_exp_for_next_level
            self.stats_dicts["level"] += 1
            self.stats_dicts["stat_points"] += 1
            if self.stats_dicts["exp_gained"] >= required_exp_for_next_level:
                self.level_up()

    def signature_effect(self, args) -> tuple:
        """
        Override this to create signature logic
        :param args: Command arguments
        :return: A tuple containing the flavor text, and if the action was successful
        """
        return "", False

    def load_saved_data(self, data: dict):
        """Load a Character"""
        self.character_name = data["name"]
        self.stats_dicts = data["stats"]

    def map_to_savable_dict(self):
        if self.current_player_actor:
            self.stats_dicts = self.current_player_actor.map_stats_to_savable_dict()
        return {
            "name": self.character_name,
            "class_name": self.class_name,
            "stats": self.stats_dicts
        }

    def set_energy_cost_override(self, overrides):
        self._command_weight_overrides = overrides

    def get_energy_cost(self, command_name):
        """
        Gets the special energy cost of a certain command if an override exists
        :param command_name: The command name to check for
        :return: The energy cost, or the default energy cost
        """
        command = command_registry[command_name.lower()]
        return self._command_weight_overrides.get(command_name, command.energy_cost())

    def get_stats_string(self) -> str:
        """Returns a string of the characters stats"""
        stats_string = ""
        if len(self.stats_dicts) == 0:
            return "No stats to display"
        for stat_name, stat_value in self.stats_dicts.items():
            stat_name = stat_name.replace("_", " ").title()
            stats_string += f"{stat_name}: {stat_value}\n"
        return stats_string

    def upgrade_stat(self, stat_name: str):
        """Upgrade a stat"""
        if stat_name in self.stats_dicts:
            self.stats_dicts[stat_name] += 1
            self.stats_dicts["stat_points"] -= 1
            stat_name = stat_name.replace("_", " ").title()
            return f"Upgraded {stat_name} to {self.stats_dicts[stat_name]}. You now have {self.stats_dicts['stat_points']} stat points remaining", True
        else:
            return "Could not upgrade that stat", False
