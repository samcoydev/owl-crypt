from dataclasses import dataclass
from typing import TYPE_CHECKING

from base.objects.actors.inventory import Inventory
from core.base.objects.actor import Actor

if TYPE_CHECKING:
    from stock.components.base.room_base import RoomBase
    from core.base.objects.character import Character
    from core.base.objects.user import User
    from core.engine import engine as e


@dataclass
class PlayerActor(Actor):
    """
    A class to represent a player actor

    Would not recommend modifying at this time.
    """

    def __init__(self, game_engine: 'e.Engine', user: 'User', character: 'Character', current_room: 'RoomBase') -> None:
        super().__init__(game_engine, current_room, character.stats_dicts["level"])
        self.user = user
        self.character = character
        self.inventory = Inventory()

    def set_health(self, hp: int):
        super().set_health(hp)
        # Do a save here maybe

    def inspect_entity(self, entity_key: str):
        """Prompt to inspect an entity by name in the players current room"""
        if entity_key == "room":
            return self.current_room.inspect_string

        return self.current_room.entities[entity_key].inspect(self)

    def interact_with_entity(self, entity_key: str) -> tuple:
        """
        Prompt to interact with an entity by name in the players current room

        :see: Entity.interact()
        :return tuple: (message, should_end_turn)
        """
        entity = self.current_room.entities[entity_key]
        if entity is None:
            return "That doesn't exist.", False

        return entity.interact(self)

    def move(self, room) -> None:
        """Move the player to a new room"""
        self.current_room = room

    def kill_entity(self) -> None:
        self.game_engine.game_manager.remove_player_actor(self.user.username)