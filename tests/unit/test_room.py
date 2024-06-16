import pytest
from core.stock.components.base.doorway_base import DoorwayBase
from core.base.types.direction_type import Direction
from tests.utils.dungeon_test_utils import DungeonTestUtils


@pytest.fixture
def setup():
    room = DungeonTestUtils.create_test_rooms()[0]()
    return room


def test_room_initialization(setup):
    room = setup
    assert room.room_name == "Test Room A"
    assert room.room_coordinates == (0, 0)
    assert room.enemies == []
    assert room.artifacts == []
    assert len(room.doorways) == 1
    assert "north" in room.doorways


def test_add_doorway(setup):
    room = setup
    new_doorway = DoorwayBase(Direction.WEST, "Wooden Door")
    room.add_doorway(new_doorway)
    assert "west" in room.doorways
