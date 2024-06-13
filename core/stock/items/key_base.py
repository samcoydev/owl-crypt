from base.objects.item import Item
from stock.components.key_door import KeyDoor


class KeyBase(Item):
    def __init__(self, name, key, description):
        super().__init__(name, key, description)

    def use(self, player_actor, args):
        """
        Use the key
        :param player_actor: the player actor
        :param args: the first argument should be a door entity key
        :return:
        """
        target = self.parse_args(player_actor, args)
        if target is None:
            return "That doesn't exist."

        # Check if the door is a subclass or class of KeyDoor
        if not isinstance(target, KeyDoor):
            return "You can't use that here."

        if target.check_key(self):
            player_actor.inventory.pop(self.key)
            return target.unlock(self, player_actor)


    def parse_args(self, player_actor, args):
        if len(args) == 0:
            return "You must specify a target to use this item on."
        key = args[0]

        return self.get_target(player_actor, key)


    def get_target(self, player_actor, key):
        return player_actor.current_room.entities.get(key, None)
