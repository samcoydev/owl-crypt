import core.stock.components.base.room_base as rb
import core.stock.components.base.doorway_base as db
import core.base.types.direction_type as dt
from stock.enemies.enemy_skeleton import SkeletonEnemy


class MainTomb(rb.RoomBase):

    def __init__(self):
        super().__init__(room_name="Main Tomb", room_coordinates=(1, 0))

    @property
    def inspect_string(self):
        return ("The smell of rot fills every corner of the room. Torch light chases away the darkness that would "
                "seemingly bring you down with it. However, the light also reveals what brings pure dread. The room is "
                "filled with coffins, some of which are open, and some of which are closed. You know somehow, they are "
                "all empty. The coffins are made of heavy stone, and are covered in moss and vines.")

    def init_doorways(self) -> None:
        self.add_doorway(db.DoorwayBase(direction=dt.Direction.WEST, inspect_string="The doorway is made up of large "
                                                                                    "wooden planks."))

    def init_enemies(self) -> None:
        self.add_enemy("skeleton", SkeletonEnemy())
