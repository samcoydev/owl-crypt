from typing import List

import core.base.objects.command as c

import core.base.objects.user as u
import engine.dungeon_registry as dungeon_registry


class Characters(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        if len(user.characters) == 0:
            return "You have no characters"

        if len(args) == 0:
            characters_string = "Characters:\n"
            for character in user.characters:
                characters_string += f"{character.character_name} - {character.class_name}\n"

            return characters_string

        character_name = " ".join(args).lower()

        for character in user.characters:
            if character.character_name.lower() == character_name:
                return character.get_stats_string()
            else:
                return "You do not have a character with that name"

    def get_help_string(self) -> str:
        return "Show the list of your characters\nCHARACTERS <name> - View a specific character's statistics"


class Difficulty(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        if args[0] == "easy":
            self.game_engine.game_manager.difficulty_multiplier = 0.5
        if args[0] == "normal":
            self.game_engine.game_manager.difficulty_multiplier = 1
        if args[0] == "hard":
            self.game_engine.game_manager.difficulty_multiplier = 1.5
        if args[0] == "nightmare":
            self.game_engine.game_manager.difficulty_multiplier = 2

    def get_help_string(self) -> str:
        return "Change the difficulty of the game\n"


class Dungeons(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        registry = dungeon_registry.dungeon_registry

        dungeons_string = "Dungeons:\n"
        if len(registry) == 0:
            dungeons_string += "No dungeons available"
            return dungeons_string

        for dungeon_technical_name in registry:
            dungeons_string += f"{registry[dungeon_technical_name].dungeon_name} - {dungeon_technical_name}\n"

        return dungeons_string

    def get_help_string(self) -> str:
        return "View a list of dungeons"


class Lobby(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        users = self.game_engine.game_manager.users_in_session.values()

        # create a string of all users in the lobby, their character, and ready status so that I can return it in full
        lobby_string = "Lobby:\n"
        if len(users) == 0:
            lobby_string += "No users in lobby"
            return lobby_string

        for _user in users:
            lobby_string += f"{_user.username} - "
            if _user.chosen_character is not None:
                lobby_string += f"{_user.chosen_character.character_name} - "
            if _user.is_ready:
                lobby_string += "READY\n"
            else:
                lobby_string += "NOT READY\n"

        return lobby_string

    def get_help_string(self) -> str:
        return "Show the list of players and their ready status"


class Pick(c.Command):
    def __init__(self, game_engine):
        super().__init__(game_engine=game_engine, requires_args=True)

    def execute(self, user: 'u.User', args: list):
        character_name = " ".join(args)
        return user.pick_character(character_name)

    def get_help_string(self) -> str:
        return "Pick a character to play as by name\nPICK <name> - Pick a character to play as by name"


class Ready(c.Command):
    def execute(self, user: 'u.User', args: List[str]):
        return self.game_engine.game_manager.set_user_ready(user)

    def get_help_string(self) -> str:
        return "Flag yourself as ready"


class Select(c.Command):
    def __init__(self, game_engine):
        super().__init__(game_engine=game_engine, requires_args=True)

    def execute(self, user: 'u.User', args: List[str]):
        dungeon = dungeon_registry.dungeon_registry.get(args[0])

        if dungeon is None:
            return "Please provide a valid dungeon name"

        self.game_engine.game_manager.set_dungeon(dungeon)
        return f"Selected dungeon {dungeon.dungeon_name}"

    def get_help_string(self) -> str:
        return "Select a dungeon to play in. Sets all players as unready."


class Upgrade(c.Command):
    def __init__(self, game_engine):
        super().__init__(game_engine=game_engine, requires_args=True)

    def execute(self, user: 'u.User', args: List[str]):
        if user.chosen_character is None:
            return "You must pick a character before you can upgrade any stats"

        if len(args) != 1:
            return "Please provide a stat to upgrade"

        stat_name = " ".join(args).replace(" ", "_").lower()

        if stat_name not in user.chosen_character.stats_dicts or stat_name == "stat_points":
            return "Please provide a valid stat to upgrade"

        if user.chosen_character.stats_dicts["stat_points"] <= 0:
            return "You do not have any stat points to spend"

        result = user.chosen_character.upgrade_stat(stat_name)

        user.save_user()

        return result

    def get_help_string(self) -> str:
        return "Use a stat point to upgrade the specified stat"
