import copy
from dataclasses import dataclass
from typing import TYPE_CHECKING
from base.objects.stat import Stat
from base.types.action import Action
from core.engine.command_registry import command_registry

if TYPE_CHECKING:
    from base.objects.role import Role

_DEFAULT_STATS = {
    "level": Stat("Level", 99, 1, is_upgradable=False),
    "health_points": Stat("Health Points", 10),
    "spell_points": Stat("Spell Points", 10),
    "rigidity_points": Stat("Rigidity Points", 10),
    "weight_limit": Stat("Weight Limit", 10),
    "base_attack_damage": Stat("Base Attack Damage", 10),
    "base_magic_damage": Stat("Base Magic Damage", 10),
    "stat_points": Stat("Stat Points", 99999, 0, is_upgradable=False),
    "exp_gained": Stat("Experience Points", 99999, 0, is_upgradable=False),
}


def default_stats():
    return copy.deepcopy(_DEFAULT_STATS)


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
        Increase the current level up by 1, handle experience point gain and resetting, and also give a stat point.

        When leveling up, the new experience requirement should be exponentially bigger.
        :return: An Action
        """
        self.stats_dicts["exp_gained"].value += self.current_actor.session_exp_gained
        self.current_actor.session_exp_gained = 0

        required_exp_for_next_level = self._get_new_experience_requirement(self.stats_dicts["level"].value)
        if self.stats_dicts["exp_gained"].value >= required_exp_for_next_level:
            self.stats_dicts["exp_gained"].value -= required_exp_for_next_level
            self.stats_dicts["level"].value += 1
            self.stats_dicts["stat_points"].value += 1
            required_exp_for_next_level = self._get_new_experience_requirement(self.stats_dicts["level"].value)
            if self.stats_dicts["exp_gained"].value >= required_exp_for_next_level:
                return self.level_up()
            return Action(f"You leveled up! You are now level {self.stats_dicts['level'].value}")

        return Action(f"You don't have enough experience points to level up!", False)

    def _get_new_experience_requirement(self, level):
        """
        Get an experience point requirement for the next level.

        Example:
            - Level 1 - EXP 1
            - Level 2 - EXP 2
            - Level 3 - EXP 26
            - Level 4 - EXP 51

        :param level: The current level
        :return int: The next experience point requirement for the next level.
        """
        return round((4 * (level ** 3)) / 5)

    def load_saved_data(self, data: dict):
        """
        Load a saved data sheet.

        :param data: The data to load
        :return: None
        """
        self.name = data["name"]
        for key, val in data["stats"].items():
            self.stats_dicts[key].value = val

    def get_energy_cost(self, command_name):
        """
        Gets the special energy cost of a certain command if an override exists
        :param command_name: The command name to check for
        :return: The energy cost, or the default energy cost
        """
        command = command_registry[command_name.lower()]
        return self.role.command_weight_overrides.get(command_name, command.energy_cost)

    def set_stats(self, stats: dict):
        """
        Set the Data Sheets stats dict
        :param stats: The stats to set
        :return: None
        """
        self.stats_dicts = stats

    def get_stats_string(self) -> str:
        """
        Gets a display string for the data sheet stats.
        :return: A string representation of the data sheet
        """
        stats_string = ""
        if len(self.stats_dicts) == 0:
            return "No stats to display"
        for _, stat in self.stats_dicts.items():
            stats_string += f"{stat.name}: {stat.value}\n"
        return stats_string

    def upgrade_stat(self, stat_name: str):
        """
        Upgrade a stat using a stat point
        :param stat_name: The name of the stat to upgrade
        :return: The resulting Action
        """
        stat_to_upgrade = self.stats_dicts[stat_name]
        if self.stats_dicts["stat_points"].value == 0:
            return Action(f"You don't have enough stat points to upgrade that.", False)

        if not stat_to_upgrade.is_upgradable:
            return Action(f"You can't upgrade that stat.", False)

        if stat_name in self.stats_dicts:
            stat_to_upgrade.value += 1
            self.stats_dicts["stat_points"].value -= 1
            return Action(
                f"Upgraded {stat_name} to {stat_to_upgrade.value}. You now have {self.stats_dicts['stat_points']} stat points remaining")

        return Action("Could not upgrade that stat.", False)
