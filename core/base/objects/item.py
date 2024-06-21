

PLACEHOLDER_MESSAGE = "Please implement the use method for this item."

class Item:
    def __init__(self, name, key, description):
        self.name = name
        self.key = key
        self.description = description

    def use(self, player_actor, args=None) -> str:
        """
        Use the item
        :param player_actor: the player actor using the item
        :param args: a list of objects
        :return: a string
        """
        return PLACEHOLDER_MESSAGE