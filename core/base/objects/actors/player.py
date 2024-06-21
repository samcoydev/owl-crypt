from dataclasses import dataclass
from typing import TYPE_CHECKING

from core.base.objects.actor import Actor
from core.stock.items.item_artifact import ItemArtifact

if TYPE_CHECKING:
    from core.stock.components.base.room_base import RoomBase
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
        self.character.current_player_actor = self
        self.inventory = {}
        self.max_inventory_size = 5

        self.max_energy_points = 5
        self.energy_points = 0
        self.used_normal = False

    def start_turn(self):
        self.energy_points = self.max_energy_points
        self.used_normal = False
        self.signature_uses = 0

    def set_health(self, hp: int):
        super().set_health(hp)
        # Do a save here maybe

    def inspect_entity(self, entity_key: str):
        """Prompt to inspect an entity by name in the players current room"""
        if entity_key == "room":
            return self.current_room.inspect_string, True

        return self.current_room.entities[entity_key].inspect(self), True

    def interact_with_entity(self, entity_key: str) -> tuple:
        """
        Prompt to interact with an entity by name in the players current room

        :see: Entity.interact()
        :return tuple: (message, should_end_turn)
        """
        entity = self.current_room.entities.get(entity_key)
        if entity is None:
            return "That doesn't exist.", False

        return entity.interact(self)

    def move(self, room) -> None:
        """Move the player to a new room"""
        self.current_room = room

    def kill_entity(self) -> None:
        self.game_engine.game_manager.remove_player_actor(self.user.username)

    def add_to_inventory(self, item_key: str, item):
        """Add an item to the players inventory"""
        if len(self.inventory) >= self.max_inventory_size:
            return "Your inventory is full.", False
        self.inventory[item_key] = item
        return f"* You picked up __{item.name}__", True

    def remove_from_inventory(self, item_key: str):
        """Remove an item from the players inventory"""
        if item_key in self.inventory:
            del self.inventory[item_key]
        else:
            return "You don't have that item.", False
        return f"* You dropped __{item_key}__", True

    def drop_item(self, item_key: str):
        item = self.inventory.get(item_key)
        msg, was_successful = self.remove_from_inventory(item_key)
        if was_successful:
            item_artifact = ItemArtifact(item, item_key, True)
            self.current_room.artifacts.append(item_artifact)
            drop_msg = f"* {self.character.character_name} dropped {item_key}"
            self.game_engine.game_manager.broadcast_to_room(drop_msg, self.current_room, self)
        return msg, was_successful

    def give_item(self, item_key: str, target_player_name):
        """Give an item to another player"""
        if item_key not in self.inventory:
            return "You don't have that item.", False

        target_player = self.game_engine.game_manager.get_player_in_room_by_character_name(self.current_room,
                                                                                           target_player_name)
        item = self.inventory[item_key]
        msg, was_successful = target_player.add_to_inventory(item_key, item)
        if was_successful:
            self.remove_from_inventory(item_key)
            return f"* You gave {target_player.character.character_name} {item.name}", True
        return f"* You couldn't give {target_player.character.character_name} {item.name}", False

    def get_inventory_string(self):
        """Get the players inventory"""
        return f"--== Inventory {self.get_remaining_space_string()} ==--\n" + '\n'.join(
            [item.name for item in self.inventory.values()]), True

    def get_remaining_space_string(self):
        return f"({len(self.inventory)}/{self.max_inventory_size})"

    def use_item(self, item_key: str, args: list):
        """Use an item from the players inventory"""
        if item_key not in self.inventory:
            return "You don't have that item.", False

        return self.inventory[item_key].use(self, args), True

    def can_afford_energy_cost(self, cmd_name):
        energy_cost = self.character.get_energy_cost(cmd_name.lower())
        return (self.energy_points > 0) and (self.energy_points - energy_cost) >= 0

    def spend_energy_points(self, cmd_name):
        command_name = cmd_name.lower()
        energy_cost = self.character.get_energy_cost(command_name)

        if self.signature_uses < self.character.signature_max and command_name.lower() is not "use":
            self.signature_uses += 1
            if not self.used_normal:
                self.used_normal = True

        self.energy_points -= energy_cost

    def block(self) -> tuple:
        return "Blocked!", True
