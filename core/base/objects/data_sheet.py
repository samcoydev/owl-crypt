from dataclasses import dataclass
from typing import TYPE_CHECKING
from base.objects.stat import Stat
from base.types.action import Action
from core.engine.command_registry import command_registry

if TYPE_CHECKING:
    from base.objects.role import Role

DEFAULT_STATS = {
    "health_points": Stat("Health Points", 10, 10),
    "spell_points": Stat("Spell Points", 10, 10),
    "rigidity_points": Stat("Rigidity Points", 10, 10),
    "weight_limit": Stat("Weight Limit", 10, 10),
    "base_attack_damage": Stat("Base Attack Damage", 10, 10),
    "base_magic_damage": Stat("Base Magic Damage", 10, 10),
    "stat_points": Stat("Stat Points", 10, 10),
    "exp_gained": Stat("Experience Points", 10, 10),
}


@dataclass
class DataSheet:
    """
    A container representing something akin to a table-top RPG character sheet. This contains the statistics
    for a controllable object, or actor.
    """
    name: str
    role: 'Role'
    current_actor = None
    stats_dicts: dict = None

    def level_up(self):
        """
        Increase the current level up by 1, handle experience point gain and resetting, and also give a stat point
        :return: None
        """
        self.stats_dicts["exp_gained"] += self.current_actor.session_exp_gained
        self.current_actor.session_exp_gained = 0

        required_exp_for_next_level = int((50 * self.stats_dicts["level"] + 1) ^ 1.2)
        if self.stats_dicts["exp_gained"] >= required_exp_for_next_level:
            self.stats_dicts["exp_gained"] -= required_exp_for_next_level
            self.stats_dicts["level"] += 1
            self.stats_dicts["stat_points"] += 1
            if self.stats_dicts["exp_gained"] >= required_exp_for_next_level:
                self.level_up()

    def load_saved_data(self, data: dict):
        """Load a Character"""
        self.name = data["name"]
        self.stats_dicts = data["stats"]

    def set_energy_cost_override(self, overrides):
        self._command_weight_overrides = overrides

    def get_energy_cost(self, command_name):
        """
        Gets the special energy cost of a certain command if an override exists
        :param command_name: The command name to check for
        :return: The energy cost, or the default energy cost
        """
        command = command_registry[command_name.lower()]
        return self._command_weight_overrides.get(command_name, command.energy_cost)

    def get_stats_string(self) -> str:
        """
        Gets a display string for the data sheet stats.
        :return: A string representation of the data sheet
        """
        stats_string = ""
        if len(self.stats_dicts) == 0:
            return "No stats to display"
        for stat_name, stat_value in self.stats_dicts.items():
            stat_name = stat_name.replace("_", " ").title()
            stats_string += f"{stat_name}: {stat_value}\n"
        return stats_string

    def upgrade_stat(self, stat_name: str):
        """
        Upgrade a stat using a stat point
        :param stat_name: The name of the stat to upgrade
        :return: The resulting Action
        """
        if stat_name in self.stats_dicts:
            self.stats_dicts[stat_name] += 1
            self.stats_dicts["stat_points"] -= 1
            stat_name = stat_name.replace("_", " ").title()
            return Action(f"Upgraded {stat_name} to {self.stats_dicts[stat_name]}. You now have {self.stats_dicts['stat_points']} stat points remaining")
        else:
            return Action("Could not upgrade that stat", False)
