from typing import List

import core.base.objects.command as c
import core.base.objects.user as u
from core.engine.command_registry import command_registry


class Attack(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        if len(args) > 0:
            enemy_name = args[0]
            return f"Attack a {enemy_name}", True

        return "Attack", True

    def get_help_string(self) -> str:
        return "Attack an enemy with your physical weapon\nATTACK - Attack an enemy by name with your " \
               "physical weapon, as long as you're outside of an encounter"


class Block(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        return f"Block for {user.player_actor.character_name}", True

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
   # TODO: Make the help command reference the docs instead. And build in a Markdown processor to the text system.

    def execute(self, user: 'u.User', args: List[str]):
        if len(args) > 0:
            return self.compose_detailed_help_string(args[0]), True

        return self.compose_help_string(), True

    def get_tutorial_str(self) -> str:
        return (
            "=== Welcome to __Owl Crypt__! ===\n" +
            "This is a text-based dungeon crawler RPG you can play with your friends, and customize to your hearts " +
            "content. To get started, follow the steps listed below. If you need more detailed explanations for any " +
            "of the commands, type `HELP <command>`. " + "\n\n" +
            " 1. Create a character by typing CHARACTERS CREATE `name` `class`.\n" +
            " 2. Pick a character by typing `PICK <name>`.\n" +
            " 3. Select a dungeon by typing `SELECT <dungeon>`.\n" +
            " 4. Wait until all players are ready. Mark yourself as ready with the `READY` command.\n" +
            " 5. Start the game by typing `START`."
        )

    def compose_detailed_help_string(self, command_name) -> str:
        if command_name.lower() == "tutorial":
            return self.get_tutorial_str()
        if command_name in command_registry:
            return command_registry[command_name].get_detailed_help_string()
        else:
            return f"Command {command_name} not found. Type HELP to see a list of available commands."

    def compose_help_string(self) -> str:
        help_string = "".join(
            [f"{command_name.upper()} - {command_registry[command_name].get_help_string()}\n" for command_name in
             command_registry])

        return help_string

    def get_help_string(self) -> str:
        return "Show the list of possible commands"

    def get_detailed_help_string(self) -> str:
        return "HELP - Show the list of possible commands\nHELP <command> - Show detailed help for a specific command\n"


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

        return response

    def get_help_string(self) -> str:
        return "Interact with an object"

    def get_detailed_help_string(self) -> str:
        return "INTERACT <name> - Interact with an object by name\n" \


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

    @property
    def energy_cost(self):
        return 1

    def get_help_string(self) -> str:
        return "Use an item from your inventory by name"

    def get_detailed_help_string(self) -> str:
        return "USE <item_name> - Use an item from your inventory by name\n"
