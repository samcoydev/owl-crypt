from typing import List

import engine.commands.command as c

import engine.objects.user as u
import dungeon_registry
from app import game_engine


@game_engine.register_command()
class Characters(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        print("Characters")

    def get_help_string(self) -> str:
        return "Show the list of your characters\nCHARACTERS <name> - View a specific character's statistics"


@game_engine.register_command()
class Dungeons(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        print("Dungeons")

    def get_help_string(self) -> str:
        return "View a list of dungeons"


@game_engine.register_command()
class Lobby(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        if user is not None:
            print("You are not in the lobby")
            return

        print("Lobby")

    def get_help_string(self) -> str:
        return "Show the list of players and their ready status"


@game_engine.register_command()
class Pick(c.Command):
    def execute(self, user: 'u.User', args: list):
        print("Pick")

    def get_help_string(self) -> str:
        return "Pick a character to play as by name\nPICK <name> - Pick a character to play as by name"


@game_engine.register_command()
class Ready(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        print("Ready")

    def get_help_string(self) -> str:
        return "Flag yourself as ready"


@game_engine.register_command()
class Select(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        if args is None or len(args) == 0:
            print("Please provide the dungeon name")
            return

        dungeon = dungeon_registry[args[0]]
        if dungeon is None:
            print("Please provide a valid dungeon name")
            return

        self.game_manager.set_dungeon(dungeon)
        print("Select")

    def get_help_string(self) -> str:
        return "Select a dungeon to play in. Sets all players as unready."
