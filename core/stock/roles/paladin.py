from base.objects.role import Role
from base.types.action import Action


class Paladin(Role):
    def __init__(self):
        super().__init__(name="paladin", signature_command_name="block", signature_max=2)

    def signature_effect(self, actor, args: list):
        """
        The Paladins signature effect is a BLOCK. The Paladin is able to block themselves
        OR another player in the same room.
        """
        manager = actor.game_engine.game_manager
        room = actor.current_room

        if len(args) > 0:
            target_name = args[0]
            target_actor = manager.get_player_in_room_by_character_name(room, target_name)
            if target_actor is None:
                return Action("Couldn't find that player.", False)
            target_actor.block()
            return Action(f"You shield your friend, {target_actor.character.character_name}!")
        else:
            return actor.block()
