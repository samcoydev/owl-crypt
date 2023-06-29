import unittest
from unittest.mock import Mock
from dungeon_modules.base.types.direction_type import Direction
from engine.objects.actors.player import PlayerActor
from dungeon_modules.base.dungeon_pieces.room_base import RoomBase
from dungeon_modules.base.dungeon_pieces.doorway_base import DoorwayBase
from tests.utils.dungeon_test_utils import DungeonTestUtils


class TestDoorwayBase(unittest.TestCase):
    def setUp(self) -> None:
        self.inspect_string = "This is a test doorway"
        self.doorway = DoorwayBase(Direction.NORTH, self.inspect_string)

    def test_init(self):
        self.assertEqual(self.doorway.direction, Direction.NORTH)
        self.assertEqual(self.doorway.inspect_string, self.inspect_string)

    # TODO: Test traversing. Needs a system for players moving between rooms

    def test_get_room_on_other_side(self):
        self.dungeon = DungeonTestUtils.create_test_dungeon("Test Dungeon")
        self.dungeon.setup_dungeon()

        self.assertEqual(self.doorway._get_room_on_other_side(self.dungeon.rooms[(0, 0)]), self.dungeon.rooms[(0, 1)])


if __name__ == "__main__":
    unittest.main()
