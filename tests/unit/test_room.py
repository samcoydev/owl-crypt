import unittest

from stock.components.base.doorway_base import DoorwayBase
from core.base.types.direction_type import Direction
from tests.utils.dungeon_test_utils import DungeonTestUtils


class RoomBaseTestCase(unittest.TestCase):
    def setUp(self):
        self.dungeon = DungeonTestUtils.create_test_dungeon("Test Dungeon")
        self.room = DungeonTestUtils.create_test_rooms()[0](self.dungeon)

    def test_room_initialization(self):
        self.assertEqual(self.room.room_name, "Test Room A")
        self.assertEqual(self.room.room_coordinates, (0, 0))
        self.assertEqual(self.room.enemies, [])
        self.assertEqual(self.room.artifacts, [])
        self.assertEqual(len(self.room.doorways), 1)
        self.assertIsNotNone(self.room.dungeon)
        self.assertTrue(self.room.doorways["north"])

    def test_add_doorway(self):
        self.new_doorway = DoorwayBase(Direction.WEST, "Wooden Door")
        self.room.add_doorway(self.new_doorway)
        self.assertTrue(self.room.doorways["west"])

if __name__ == "__main__":
    unittest.main()