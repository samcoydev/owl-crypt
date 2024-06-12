import core.stock.components.room_base as rb
import core.stock.components.doorway_base as db
import core.base.types.direction_type as dt


class StarterRoom(rb.RoomBase):

    def __init__(self):
        super().__init__(room_name="The Entrance", room_coordinates=(0, 0))

    @property
    def inspect_string(self) -> str:
        return ("The room sits dark, with dimly lit torches lighting the archways. The room smells of wet stone and "
                "moss. Things are moving in the dark, only to hide between the stone slabs in the wall.")

    def init_doorways(self) -> None:
        self.add_doorway(db.DoorwayBase(direction=dt.Direction.EAST,
                                        inspect_string="The doorway is made up of large wooden planks, with torch "
                                                       "light breaking through the cracks."))
