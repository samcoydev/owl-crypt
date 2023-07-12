from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.stock.components.room_base import RoomBase
    from core.engine.engine import Engine


@dataclass(kw_only=True)
class Actor(ABC):
    """
    An actor takes the abstract idea of an entity and gives it a representation in the game world. Think Players,
    Enemies, etc.

    Would not recommend modifying at this time.
    """

    game_engine: 'Engine'
    current_room: 'RoomBase'

    level: int
    health_points: int = 1
    spell_points: int = 1
    rigidity_points: int = 1
    weight_limit: int = 1
    base_attack_damage: int = 1
    base_magic_damage: int = 1
    stat_points: int = 0
    exp_gained: int = 0
    session_exp_gained: int = 0

    current_target: 'Actor' or None = None

    def __post_init__(self):
        self.current_target = None

    def deal_damage(self, damage: int):
        """
        Deal damage to health points with rigidity factored in
        """
        dmg_to_deal = damage - self.rigidity_points
        if dmg_to_deal < 0:
            dmg_to_deal = 1
        self.deal_pure_damage(dmg_to_deal)

    def deal_pure_damage(self, damage: int):
        """
        Deal damage to health points without rigidity factored in
        :param damage:
        :return:
        """
        self.set_health(self.health_points - damage)

        if self.health_points <= 0:
            self.kill_entity()

    def set_health(self, hp: int):
        self.health_points = hp

    def map_stats_to_savable_dict(self):
        return {
            "health_points": self.health_points,
            "spell_points": self.spell_points,
            "rigidity_points": self.rigidity_points,
            "weight_limit": self.weight_limit,
            "base_attack_damage": self.base_attack_damage,
            "base_magic_damage": self.base_magic_damage,
            "stat_points": self.stat_points,
            "exp_gained": self.exp_gained
        }

    def set_stats(self, stats_dict):
        """
        Set the stats of an actor with level and difficulty scaling.
        :param stats_dict: The stats to set
        """
        for stat_name, stat_value in stats_dict.items():
            stats_dict[stat_name] = self.scale_stat_level(stat_value)
        self._set_stats(stats_dict)

    def _set_stats(self, stats_dict):
        """
        Set the stats of an actor without scaling.
        :param stats_dict: The stats to set
        """
        self.health_points = stats_dict["health_points"]
        self.spell_points = stats_dict["spell_points"]
        self.rigidity_points = stats_dict["rigidity_points"]
        self.weight_limit = stats_dict["weight_limit"]
        self.base_attack_damage = stats_dict["base_attack_damage"]
        self.base_magic_damage = stats_dict["base_magic_damage"]
        self.stat_points = stats_dict["stat_points"]
        self.exp_gained = stats_dict["exp_gained"]

    def scale_stat_level(self, stat_value: int):
        """
        Scale a stat value based on the difficulty mode. Defaulted to "Normal"
        :param stat_value:
        :return: Scaled stat value
        """
        difficulty_multiplier = 1
        return (stat_value * 10) * difficulty_multiplier

    @abstractmethod
    def kill_entity(self) -> None:
        raise NotImplementedError("Please implement kill_entity")
