import pytest
from core.base.types.direction_type import Direction
from core.stock.components.base.doorway_base import DoorwayBase
from tests.utils.dungeon_test_utils import DungeonTestUtils


# setup function is replaced with a fixture in pytest
@pytest.fixture
def setup():
    inspect_string = "This is a test doorway"
    doorway = DoorwayBase(Direction.NORTH, inspect_string)
    return inspect_string, doorway


def test_init(setup):
    inspect_string, doorway = setup
    assert doorway.direction == Direction.NORTH
    assert doorway.inspect_string == inspect_string


# TODO: Test traversing. Needs a system for players moving between rooms

def test_get_room_on_other_side(setup):
    _, doorway = setup
    dungeon = DungeonTestUtils.create_test_dungeon("Test Dungeon")
    dungeon.setup_dungeon()

    assert doorway._get_room_on_other_side(dungeon.rooms[(0, 0)]) == dungeon.rooms[(0, 1)]
