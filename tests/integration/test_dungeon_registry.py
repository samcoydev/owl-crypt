import unittest

import core.engine.dungeon_registry as dungeon_registry
from tests.utils.dungeon_test_utils import DungeonTestUtils


def test_dungeon_and_rooms_integration(game_engine):
    dungeon = DungeonTestUtils.create_test_dungeon("Test Dungeon")
    dungeon.setup_dungeon(game_engine.game_manager)

    dungeon_registry.register_dungeon(dungeon)

    assert dungeon_registry.dungeon_registry["test_dungeon"] == dungeon
