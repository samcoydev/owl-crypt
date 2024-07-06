from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from base.constants import NON_EXISTENT
from base.types.action import Action
from core.engine.status_registry import status_registry
from stock.items.item_artifact import ItemArtifact

if TYPE_CHECKING:
    from engine.engine import Engine
    from stock.components.base.room_base import RoomBase
    from base.objects.data_sheet import DataSheet


@dataclass
class Actor:
    """
    An Actor is a representation of a controllable object in the game world. Actors interact with other actors to
    change their `sheet` data.
    """
    game_engine: 'Engine'
    current_room: 'RoomBase'
    data_sheet: 'DataSheet'

    inventory: dict = field(default_factory=dict)
    max_inventory_size: int = 5

    max_energy_points: int = 5
    energy_points: int = 0
    used_normal: bool = False
    signature_uses: int = 0

    exp_gained: int = 0
    session_exp_gained: int = 0

    active_status_effects: list = field(default_factory=list)
    current_target = None

    def __post_init__(self):
        self.data_sheet.current_actor = self
        self.current_room.actors.append(self)
        self.move(self.current_room)

    def tick(self) -> None:
        """
        Tick all events that should run at the beginning of the player turn cycle.
        :return: None
        """
        self._tick_status_effects()

    def _tick_status_effects(self) -> None:
        """
        Loops through all active status effects and applies them to the actor, while also decreasing the half-life of
        the status effect by one.

        TODO: Add a way to remove status effects from the actor
        TODO: Add a way to decrease the half-life of a status effect by a variable factor
        TODO: Add resistances to status effects
        :return: None
        """
        if self.active_status_effects is None:
            return

        for status_effect in self.active_status_effects:
            try:
                status_registry[status_effect[0]](self, status_effect[3])
                status_effect[2] -= 1
            except KeyError:
                print(f"Could not find status effect {status_effect[0]} in registry")
            if status_effect[2] <= 0:
                self.active_status_effects.remove(status_effect)

    def inflict(self, status_effect: str, duration: int, strength: int):
        """
        Inflict a status effect on the actor
        :param status_effect: The status effect to inflict
        :param duration: The duration of the status effect
        :param strength: The strength of the status effect
        :return: None
        """
        if self.active_status_effects is None:
            self.active_status_effects = []
        self.active_status_effects.append([status_effect, duration, strength])

    def deal_damage(self, damage: int):
        """
        Deal damage to health points with rigidity factored in. Damage will be subtracted by the target actors rigidity
        points, and default to 1 if the difference is equal to or less than 0.
        :param damage: The damage to deal
        :return: None
        """
        dmg_to_deal = damage - self.data_sheet.stats["rigidity_points"].value
        if dmg_to_deal < 0:
            dmg_to_deal = 1
        self.deal_pure_damage(dmg_to_deal)

    def deal_pure_damage(self, damage: int):
        """
        Deal damage to health points without rigidity factored in
        :param damage:
        :return: None
        """
        self.set_health(self.data_sheet.stats["health_points"] - damage)
        if self.data_sheet.stats["health_points"] <= 0:
            self.kill_actor()

    def heal(self, heal_amount: int):
        """
        Heal the actor by a certain amount
        :param heal_amount: The amount to heal
        :return: None
        """
        self.set_health(self.data_sheet.stats["health_points"] + heal_amount)

    def set_health(self, hp: int) -> None:
        """
        Set the actors health
        :param hp: number to set the health to
        :return: None
        """
        self.data_sheet.set_stat("health_points", hp)

    def start_turn(self):
        self.energy_points = self.max_energy_points
        self.used_normal = False
        self.signature_uses = 0

    def inspect_entity(self, entity_key: str):
        """Prompt to inspect an entity by name in the actors current room"""
        if entity_key == "room":
            return self.current_room.inspect_string, True

        return self.current_room.entities[entity_key].inspect(self), True

    def interact_with_entity(self, entity_key: str) -> tuple:
        """
        Prompt to interact with an entity by name in the actors current room

        :see: Entity.interact()
        :return tuple: (message, should_end_turn)
        """
        entity = self.current_room.entities.get(entity_key)
        if entity is None:
            return NON_EXISTENT, False

        return entity.interact(self)

    def move(self, room) -> None:
        """
        Move the actor to a new room
        :param room: The room to move
        :return: None
        """
        self.current_room.actors.remove(self)
        self.current_room = room
        self.current_room.actors.append(self)

    def kill_actor(self) -> None:
        """
        Kill the actor
        :return: None
        """
        pass

    def add_to_inventory(self, item_key: str, item):
        """
        Add an item to the actors inventory
        :param item_key: The key of the item
        :param item: The item to add
        :return Action: The resulting Action
        """
        if len(self.inventory) >= self.max_inventory_size:
            return Action("Your inventory is full.", False)
        self.inventory[item_key] = item
        return Action(f"* You picked up __{item.name}__")

    def remove_from_inventory(self, item_key: str):
        """
        Remove an item from the actors inventory.
        :param item_key: The item to remove
        :return Action: The resulting Action
        """
        if item_key in self.inventory:
            del self.inventory[item_key]
            return Action(f"* You dropped __{item_key}__")
        return Action("You don't have that item.", False)

    def drop_item(self, item_key: str):
        """
        Drop an item in the actors inventory into the current room.
        :param item_key: The key of the item to drop
        :return Action: The resulting Action
        """
        item = self.inventory.get(item_key)
        action = self.remove_from_inventory(item_key)
        if action.was_successful:
            item_artifact = ItemArtifact(item, item_key, True)
            self.current_room.artifacts.append(item_artifact)
            drop_msg = f"* {self.data_sheet.name} dropped {item_key}"
            self.game_engine.game_manager.broadcast_to_room(drop_msg, self.current_room, self)
        return action

    def give_item(self, item_key: str, target_actor_name):
        """
        Give an item to another actor
        :param item_key: The key of the item to give
        :param target_actor_name: The name of the actors data sheet to give the item
        :return Action: The resulting Action
        """
        if item_key not in self.inventory:
            return Action("You don't have that item.", False)

        target_actor = self.current_room.get_actor_by_name(target_actor_name)
        if target_actor is None:
            return Action("Couldn't recognize that name.", False)

        item = self.inventory[item_key]
        action = target_actor.add_to_inventory(item_key, item)
        if action.was_successful:
            self.remove_from_inventory(item_key)
            return Action(f"* You gave {target_actor.data_sheet.name} {item.name}")
        return Action(f"* You couldn't give {target_actor.data_sheet.name} {item.name}", False)

    def get_inventory_string(self):
        """
        Get the actors inventory
        :return str: The display string for the actors inventory
        """
        return f"--== Inventory {self.get_remaining_space_string()} ==--\n" + '\n'.join(
            [item.name for item in self.inventory.values()]), True

    def get_remaining_space_string(self):
        """
        Get a display string for the remaining space in the actors inventory
        :return str: The display string
        """
        return f"({len(self.inventory)}/{self.max_inventory_size})"

    def use_item(self, item_key: str, args: list):
        """
        Use an item from the actors inventory
        :param item_key: The key of the item to use
        :param args: The arguments passed with the command
        :return Action: The resulting Action
        """
        if item_key not in self.inventory:
            return Action("You don't have that item.", False)
        return Action(self.inventory[item_key].use(self, args))

    def can_call_command(self, cmd_name):
        """
        Check if the actor can run a command. Refer to the [[Command Weight]] page in the docs for more information on
        command weight.
        :param cmd_name: The name of the command to run
        :return bool: If the command can be called
        """
        command_name = cmd_name.lower()

        # Use can be used at any point
        if command_name == "use":
            return True

        if self.used_normal:
            if command_name == self.data_sheet.role.signature_command_name:
                if self.signature_uses < self.data_sheet.role.signature_max:
                    return True
            return False


    def can_afford_energy_cost(self, cmd_name):
        """
        Check if the actor has enough energy points to afford a commands energy cost.
        :param cmd_name: The name of the command to check for
        :return bool: Whether the actor can afford the energy cost
        """
        energy_cost = self.data_sheet.get_energy_cost(cmd_name.lower())
        return (self.energy_points > 0) and (self.energy_points - energy_cost) >= 0

    def spend_energy_points(self, cmd_name):
        """
        Decrement the amount of energy points spent by a commands energy cost.
        :param cmd_name: The command being run
        :return: None
        """
        command_name = cmd_name.lower()
        energy_cost = self.data_sheet.get_energy_cost(command_name)

        if self.signature_uses < self.data_sheet.role.signature_max and command_name.lower() is not "use":
            self.signature_uses += 1
            if not self.used_normal:
                self.used_normal = True

        self.energy_points -= energy_cost

    def attack(self, actor_id):
        """
        Attack an actor by id
        :param actor_id: The id of the actor to attack
        :return Action: The resulting Action
        """
        pass

    def block(self):
        """
        Cause the actor to block
        :return Action: The resulting Action
        """
        return Action("Blocked!")