from engine.objects.characters.character import Character
from engine.objects.characters.character_registry import register_character_class
from engine.commands.vanilla_game_commands import Block


@register_character_class()
class Paladin(Character):

    def __init__(self, character_name: str):
        # This is where we could set Paladin specific stats. Paladins could start with a higher hp for example.
        super().__init__(character_name, self.__class__.__name__.lower(), Block.__name__, 2)

        self._special_effects = {Block.__name__: self.block_special}

    def block_special(self, command_name: str, args: list):
        if len(args) > 0:
            target_actor = self.current_player_actor.game_engine.game_manager.player_actors[args[0]]
            if target_actor is not None:
                command = self.current_player_actor.game_engine.command_registry[command_name.lower()]
                command.execute(target_actor.character, args)
                return

        command = self.current_player_actor.game_engine.command_registry[command_name.lower()]
        command.execute(self, args)
        return
