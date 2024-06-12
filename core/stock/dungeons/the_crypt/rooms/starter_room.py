import core.stock.components.room_base as rb
import core.stock.components.doorway_base as db
import core.base.types.direction_type as dt


class StarterRoom(rb.RoomBase):

    def __init__(self):
        super().__init__(room_name="The Entrance", room_coordinates=(0, 0))

    @property
    def inspect_string(self) -> str:
        return ("The room sits dark, with dimly lit torches lighting the archways. The room smells of wet stone and "
                "moss. Things are moving in the dark, only to hide between the stone slabs in the wall before you can"
                "make sense of them.")

    def get_first_visit_text(self) -> str:
        return ("\n\nYou notice a __Door on the East side of the room__. You can see a faint light coming from the other side.")

    def init_doorways(self) -> None:
        self.add_doorway(db.DoorwayBase(direction=dt.Direction.EAST,
                                        inspect_string="The doorway is made up of large wooden planks, with torch "
                                                       "light breaking through the cracks."))
