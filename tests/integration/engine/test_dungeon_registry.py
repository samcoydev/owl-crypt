import unittest

import engine.dungeon_registry as dungeon_registry
from tests.utils.dungeon_test_utils import DungeonTestUtils


class TestDungeonRegistry(unittest.TestCase):

    def test_dungeon_and_rooms_integration(self):
        # Create and register a test dungeon
        self.dungeon = DungeonTestUtils.create_test_dungeon("Test Dungeon")
        self.dungeon.setup_dungeon()

        dungeon_registry.register_dungeon("Test Dungeon")(self.dungeon)

        self.assertEqual(dungeon_registry.dungeon_registry["Test Dungeon"], self.dungeon)
