from stock.components.base.doorway_base import DoorwayBase


class KeyDoor(DoorwayBase):
    """A reusable class to create dungeon doorways that require keys"""

    def __init__(self, direction, inspect_string, required_key: str) -> None:
        super().__init__(direction, inspect_string)
        self.required_key = required_key
        self.locked = True

    def can_traverse(self, player) -> bool:
        if self.locked:
            return False
        return super().can_traverse(player)

    def get_failed_traverse_message(self, player=None) -> str:
        if self.locked:
            return "The door is locked."
        return super().get_failed_traverse_message(player)

    def unlock(self, key, actor=None):
        self.locked = False
        return f"You unlock the door with the {key.name}."

    def check_key(self, key):
        return key.key == self.required_key
