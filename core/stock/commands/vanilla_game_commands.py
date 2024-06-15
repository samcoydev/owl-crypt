from typing import List

import core.base.objects.command as c
import core.base.objects.user as u
from engine.command_registry import command_registry


class Attack(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        if len(args) > 0:
            enemy_name = args[0]
            print(f"Attack a {enemy_name}")

        print("Attack")

    def get_help_string(self) -> str:
        return "Attack an enemy with your physical weapon\nATTACK - Attack an enemy by name with your " \
               "physical weapon, as long as you're outside of an encounter"


class Block(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        print(f"Block for {user.character_name}")

    def get_help_string(self) -> str:
        return "Build up defense in battle"


class Cast(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        print("Cast")

    def get_help_string(self) -> str:
        return "Cast a spell from your spellbook by name"


class Drop(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        item_key = args[0]
        return user.player_actor.drop_item(item_key)

    def get_help_string(self) -> str:
        return "Drop an item from your inventory by name"


class Give(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        item_key = args[0]
        target_player = args[1]
        return user.player_actor.give_item(item_key, target_player)

    def get_help_string(self) -> str:
        return "Give an item from your inventory by name to a player by name"


class Help(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        help_string = "".join(
            [f"{command_name.upper()} - {command_registry[command_name].get_help_string()}\n" for command_name in
             command_registry])

        return help_string

    def get_help_string(self) -> str:
        return "Show the list of possible commands"


class Inspect(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        target = args[0] if len(args) > 0 else "room"
        return user.player_actor.inspect_entity(target)

    def get_help_string(self) -> str:
        return "Inspect an object"


class Interact(c.Command):
    def __init__(self, game_engine, command_type: str = "game", requires_args: bool = True):
        super().__init__(game_engine, command_type, requires_args)

    def execute(self, user: 'u.User', args: List[str]):
        target = args[0]
        response = user.player_actor.interact_with_entity(target)
        if response is None:
            return "That doesn't exist."
        elif response[1]:
            self.game_engine.game_manager.next_player_turn()

        return response[0]

    def get_help_string(self) -> str:
        return "Interact with an object"


class Inventory(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        return user.player_actor.get_inventory_string()

    def get_help_string(self) -> str:
        return "View your inventory"


class Sneak(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        print("Sneak")

    def get_help_string(self) -> str:
        return "Roll an chance to sneak"


class SpellBook(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        print("SpellBook")

    def get_help_string(self) -> str:
        return "View your spellbook"


class Use(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        item_key = args[0]
        return user.player_actor.use_item(item_key, args[1:])

    def get_help_string(self) -> str:
        return "Use an item from your inventory by name"
