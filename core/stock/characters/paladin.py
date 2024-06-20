from core.base.objects.character import Character, get_base_stats


class Paladin(Character):
    def __init__(self, character_name: str):
        # This is where we could set Paladin specific stats. Paladins could start with a higher hp for example.
        super().__init__(character_name, self.__class__.__name__.lower(), "block", 2)

        self.stats_dicts = get_base_stats()

    def signature_effect(self, args: list):
        """
        The Paladins signature effect is a BLOCK. The Paladin is able to block themselves
        OR another player in the same room.
        """
        manager = self.current_player_actor.game_engine.game_manager
        room = self.current_player_actor.current_room

        # Trying to block someone else
        if len(args) > 0:
            target_name = args[0]
            target_actor = manager.get_player_in_room_by_character_name(room, target_name)
            if target_actor is None:
                return "Couldn't find that player.", False
            target_actor.block()
            return f"You shield your friend, {target_actor.character.character_name}!", True
        else:
            return self.current_player_actor.block()

