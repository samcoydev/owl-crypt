from typing import List

import engine.commands.command as c
import engine.objects.user as u
from app import game_engine


@game_engine.register_command()
class Attack(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        if len(args) > 0:
            enemy_name = args[0]
            print(f"Attack a {enemy_name}")

        print("Attack")

    def get_help_string(self) -> str:
        return "Attack an enemy with your physical weapon\nATTACK - Attack an enemy by name with your " \
               "physical weapon, as long as you're outside of an encounter"


@game_engine.register_command()
class Block(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        print(f"Block for {user.character_name}")

    def get_help_string(self) -> str:
        return "Build up defense in battle"


@game_engine.register_command()
class Cast(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        print("Cast")

    def get_help_string(self) -> str:
        return "Cast a spell from your spellbook by name"


@game_engine.register_command()
class Help(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        help_string = "".join(
            [f"{command.__name__.upper()} - {command().get_help_string()}\n" for command in self.game_engine.command_registry.values()])

        return help_string

    def get_help_string(self) -> str:
        return "Show the list of possible commands"


@game_engine.register_command()
class Inspect(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        print("Inspect")

    def get_help_string(self) -> str:
        return "Inspect an object"


@game_engine.register_command()
class Interact(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        print("Interact")

    def get_help_string(self) -> str:
        return "Interact with an object"


@game_engine.register_command()
class Inventory(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        print("Inventory")

    def get_help_string(self) -> str:
        return "View your inventory"


@game_engine.register_command()
class Sneak(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        print("Sneak")

    def get_help_string(self) -> str:
        return "Roll an chance to sneak"


@game_engine.register_command()
class SpellBook(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        print("SpellBook")

    def get_help_string(self) -> str:
        return "View your spellbook"


@game_engine.register_command()
class Use(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        print("Use")

    def get_help_string(self) -> str:
        return "Use an item from your inventory by name"
