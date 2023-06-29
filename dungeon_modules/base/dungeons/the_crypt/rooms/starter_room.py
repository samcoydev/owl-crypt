import dungeon_modules.base.dungeon_pieces.room_base as rb
import dungeon_modules.base.dungeon_pieces.doorway_base as db
import dungeon_modules.base.types.direction_type as dt


class StarterRoom(rb.RoomBase):

    def __init__(self):
        super().__init__(room_name="The Entrance", room_coordinates=(0, 0))

    def view_room(self):
        return ("The room sits dark, with dimly lit torches lighting the archways. The room smells of wet stone and "
                "moss. Things are moving in the dark, only to hide between the stone slabs in the wall.")

    def init_doorways(self) -> None:
        self.add_doorway(db.DoorwayBase(direction=dt.Direction.EAST,
                                        inspect_string="The doorway is made up of large wooden planks, with torch "
                                                       "light breaking through the cracks."))
