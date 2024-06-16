import core.stock.components.base.room_base as rb
import core.stock.components.key_door as kd
import core.base.types.direction_type as dt
from core.stock.items.item_artifact import ItemArtifact
from core.stock.items.key_base import KeyBase


class StarterRoom(rb.RoomBase):

    def __init__(self):
        super().__init__(room_name="The Entrance", room_coordinates=(0, 0))
        self.init_artifacts()

    @property
    def inspect_string(self) -> str:
        return ("The room sits dark, with dimly lit torches lighting the archways. The room smells of wet stone and "
                "moss. Things are moving in the dark, only to hide between the stone slabs in the wall before you can"
                "make sense of them.")

    def get_first_visit_text(self) -> str:
        return (
            "\n\nYou notice a __Door on the East side of the room__. You can see a faint light coming from the other side.")

    def init_doorways(self) -> None:
        self.add_doorway(
            kd.KeyDoor(
                dt.Direction.EAST,
                "The doorway is made up of large wooden planks, with torch light breaking through the cracks.",
                "rusty_key"
            )
        )

    def init_artifacts(self) -> None:
        rusty_key = KeyBase("Rusty Key", "rusty_key", "It's a key. It feels fragile.")
        artifact = ItemArtifact(rusty_key, "rusty_key")

        self.artifacts.append(artifact)
