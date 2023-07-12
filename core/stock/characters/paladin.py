from core.base.objects.character import Character


class Paladin(Character):

    def __init__(self, character_name: str):
        # This is where we could set Paladin specific stats. Paladins could start with a higher hp for example.
        super().__init__(character_name, self.__class__.__name__.lower(), "block", 2)

        self._special_effects = {"block": self.block_special}

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
