from stock.components.base.doorway_base import DoorwayBase


class KeyDoor(DoorwayBase):
    """A reusable class to create dungeon doorways"""
    def __init__(self, direction: 'dr.Direction', inspect_string, required_key: str) -> None:
        super().__init__(direction, inspect_string)
        self.required_key = required_key
        self.locked = True

    def can_traverse(self, player: 'pa.PlayerActor') -> bool:
        if self.locked:
            return ("The door is locked.", False)
        return ("You move through the door.", True)

    def unlock(self, key, actor=None):
        self.locked = False
        return f"You unlock the door with the {key.name}."

    def check_key(self, key):
        return key.key == self.required_key