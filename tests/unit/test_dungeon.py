import unittest
import core.stock.components.room_base as room_base
from core.stock.components.doorway_base import DoorwayBase
from core.base.types.direction_type import Direction
from tests.utils.dungeon_test_utils import DungeonTestUtils


class TestDungeon(unittest.TestCase):

    def setUp(self) -> None:
        self.dungeon = DungeonTestUtils.create_test_dungeon("Test Dungeon")
        self.dungeon.setup_dungeon()

    def test_add_room(self):
        dungeon_ref = self.dungeon

        # Create a new room
        class TestRoom(room_base.RoomBase):
            def __init__(self):
                super().__init__(room_name="Test Room", room_coordinates=(1, 1), dungeon=dungeon_ref)

            def init_doorways(self) -> None:
                self.add_doorway(DoorwayBase(Direction.WEST, "Wooden Door"))

            def view_room(self):
                return "This is test room"

        self.new_room = TestRoom()

        self.assertEqual(len(self.dungeon.rooms), 2)

        # Add a new doorway to (0, 1) - This room is created by the dungeon util function
        self.dungeon.rooms[(0, 1)].add_doorway(DoorwayBase(Direction.EAST, "Wooden Door"))
        self.dungeon.add_room(self.new_room)

        # Now the dungeon should look like this:
        #   []-[] <-- New room at (1, 1)
        #   [] <-- Starting room at (0, 0)

        self.assertEqual(len(self.dungeon.rooms), 3)
