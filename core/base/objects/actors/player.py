from dataclasses import dataclass
from typing import TYPE_CHECKING

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
        self.inventory = {}

    def set_health(self, hp: int):
        super().set_health(hp)
        # Do a save here maybe

    def inspect_entity(self, entity_key: str):
        """Prompt to inspect an entity by name in the players current room"""
        if entity_key == "room":
            return self.current_room.inspect_string

        return self.current_room.entities[entity_key].inspect(self)

    def interact_with_entity(self, entity_key: str):
        """Prompt to interact with an entity by name in the players current room"""
        entity = self.current_room.entities[entity_key]
        if entity is None:
            return ("That doesn't exist.", False)

        return entity.interact(self)

    def add_to_inventory(self, item_key: str, item):
        """Add an item to the players inventory"""
        self.inventory[item_key] = item
        return f"* You picked up __{item.name}__"

    def get_inventory_string(self):
        """Get the players inventory"""
        return "--== Inventory ==--\n" + '\n'.join([item.name for item in self.inventory.values()])

    def use_item(self, item_key: str, args: list):
        """Use an item from the players inventory"""
        print(f"Using item {item_key} with args {args}")
        if item_key not in self.inventory:
            return "You don't have that item."

        return self.inventory[item_key].use(self, args)

    def interact_with_artifact(self, artifact_name: str) -> None:
        """Prompt to interact with an artifact by name in the players current room"""
        self.current_room.find_artifact_by_name(artifact_name).interact(self)

    def inspect_artifact(self, artifact_name: str) -> None:
        """Prompt to inspect an artifact by name in the players current room"""
        self.current_room.find_artifact_by_name(artifact_name).inspect(self)

    def kill_entity(self) -> None:
        self.game_engine.game_manager.remove_player_actor(self.user.username)