from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dungeon_modules.base.dungeon_pieces.room_base import RoomBase
    from engine.engine import Engine


class Actor(ABC):
    """
    An actor takes the abstract idea of an entity and gives it a representation in the game world. Think Players,
    Enemies, etc.
    """

    def __init__(self, game_engine: 'Engine', health: int, damage: int, current_room: 'RoomBase',
                 current_target: 'Actor' = None) -> None:
        self.game_engine = game_engine
        self.__hp = health
        self.damage = damage
        self.current_room = current_room
        self.current_target = current_target

    def deal_damage(self, damage_amount: int) -> None:
        self.set_health(self.get_health() - damage_amount)

        if self.get_health() <= 0:
            self.kill_entity()

    def get_health(self) -> int:
        return self.__hp

    def set_health(self, hp: int) -> None:
        self.__hp = hp

    @abstractmethod
    def kill_entity(self) -> None:
        raise NotImplementedError("Please implement kill_entity")
