import pytest
import core.stock.components.base.room_base as room_base
from core.stock.components.base.doorway_base import DoorwayBase
from core.base.types.direction_type import Direction
from tests.utils.dungeon_test_utils import DungeonTestUtils

@pytest.fixture
def setup():
    dungeon = DungeonTestUtils.create_test_dungeon("Test Dungeon")
    dungeon.setup_dungeon()
    return dungeon

def test_add_room(setup):
    dungeon = setup

    # Create a new room
    class TestRoom(room_base.RoomBase):
        def __init__(self):
            super().__init__(room_name="Test Room", room_coordinates=(1, 1))

        def init_doorways(self) -> None:
            self.add_doorway(DoorwayBase(Direction.WEST, "Wooden Door"))

        def view_room(self):
            return "This is test room"

    new_room = TestRoom()

    assert len(dungeon.rooms) == 2

    # Add a new doorway to (0, 1) - This room is created by the dungeon util function
    dungeon.rooms[(0, 1)].add_doorway(DoorwayBase(Direction.EAST, "Wooden Door"))
    dungeon.add_room(new_room)

    # Now the dungeon should look like this:
    #   []-[] <-- New room at (1, 1)
    #   [] <-- Starting room at (0, 0)

    assert len(dungeon.rooms) == 3