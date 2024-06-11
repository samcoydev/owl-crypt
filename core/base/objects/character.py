from abc import ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING

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
    _special_effects = {}
    signature_command_name: str
    signature_max: int

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

    def run_command(self, command_name, args):
        cmd = command_name.lower()

        # Check if the command has a special effect for this character class
        if cmd in self._special_effects:
            special_effect = self._special_effects[cmd]
            special_effect(cmd, args)
        else:
            command = self.current_player_actor.game_engine.command_registry[cmd.lower()]
            command.execute(self, args)

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
            return f"Upgraded {stat_name} to {self.stats_dicts[stat_name]}. You now have {self.stats_dicts['stat_points']} stat points remaining"
        else:
            return "Could not upgrade that stat"
