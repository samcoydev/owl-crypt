from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from dungeon_modules.base.types import elemental_type as et


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
