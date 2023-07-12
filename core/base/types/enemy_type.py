from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict

from core.base.types import elemental_type as et


class EnemyType(ABC):

    def __init__(self, name: str, base_attack: int, elemental_type: 'et.ElementalType' = None):
        self.name = name
        self.base_attack = base_attack
        self.elemental_type = elemental_type
        self.display_name = self.get_display_name_prefix()

    def get_display_name_prefix(self) -> str:
        if self.elemental_type is not None:
            return f"{self.elemental_type.name} {self.name}"

        return self.name

    def get_stat_distribution(self) -> Dict[str, int]:
        """
        Override this method to create a custom stat distribution for an enemy
        """
        return {
            "health_points": 20,
            "spell_points": 20,
            "rigidity_points": 20,
            "base_attack_damage": 20,
            "base_magic_damage": 20
        }

    def distribute_points(self, level):
        """
        Calculates the stat distribution for an enemy of a given level and stat distribution.
        Args:
          level: The level of the enemy.
        Returns:
          A dictionary of stats, where the key is the name of the stat and the value is the value of the stat.
        """
        stat_distribution: Dict[str, int] = self.get_stat_distribution()
        stats = {"weight_limit": 100}
        total_weight = sum(weight for _, weight in stat_distribution.items())
        for stat_name, weight in stat_distribution.items():
            stat_value = int(level * weight / total_weight)
            if stat_value < 1:
                stat_value = 1

            stats[stat_name] = stat_value

        return stats

    @abstractmethod
    def get_death_dialog(self) -> str:
        """Override this method to add flavor text to an enemy's death dialog"""
        raise NotImplementedError(f"Please implement a death dialog for {self.name}")

    @abstractmethod
    def get_attack_dialog(self) -> str:
        """Override this method to add flavor text to an enemy's dialog when attacking a player"""
        raise NotImplementedError(f"Please implement an attack dialog for {self.name}")

    @abstractmethod
    def get_damaged_dialog(self) -> str:
        """Override this method to add flavor text to an enemy's dialog when being damaged by the player"""
        raise NotImplementedError(f"Please implement a damaged dialog for {self.name}")

    @abstractmethod
    def get_encounter_dialog(self) -> str:
        """Override this method to add flavor text to an enemy's dialog when engaging the player"""
        raise NotImplementedError(f"Please implement an encounter dialog for {self.name}")
