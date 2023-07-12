import core.stock.components.dungeon_base as dungeon_base
import core.stock.components.room_base as room_base
import core.stock.components.doorway_base as doorway_base
import core.base.types.direction_type as direction_type
from base.types.enemy_type import EnemyType


class DungeonTestUtils:
    @staticmethod
    def create_test_dungeon(dungeon_name: str) -> 'dungeon_base.DungeonBase':
        class TestDungeon(dungeon_base.DungeonBase):
            def setup_dungeon(self):
                # Define the setup logic for the test dungeon
                self.add_room(DungeonTestUtils.create_test_rooms()[0](self))
                self.add_room(DungeonTestUtils.create_test_rooms()[1](self))

        return TestDungeon(dungeon_name)

    @staticmethod
    def create_test_rooms():
        class TestRoomA(room_base.RoomBase):
            def __init__(self, dungeon: 'dungeon_base.DungeonBase'):
                super().__init__(room_name="Test Room A", room_coordinates=(0, 0), dungeon=dungeon)

            def init_doorways(self) -> None:
                self.add_doorway(doorway_base.DoorwayBase(direction_type.Direction.NORTH, "Wooden Door"))

            def view_room(self):
                return "This is test room A"

        class TestRoomB(room_base.RoomBase):
            def __init__(self, dungeon: 'dungeon_base.DungeonBase'):
                super().__init__(room_name="Test Room B", room_coordinates=(0, 1), dungeon=dungeon)

            def init_doorways(self) -> None:
                self.add_doorway(doorway_base.DoorwayBase(direction_type.Direction.SOUTH, "Wooden Door"))

            def view_room(self):
                return "This is test room B"

        return TestRoomA, TestRoomB

    @staticmethod
    def create_test_enemy_type():
        class MockEnemyType(EnemyType):
            def get_death_dialog(self) -> str:
                return "Mock Death Dialog"

            def get_attack_dialog(self) -> str:
                return "Mock Attack Dialog"

            def get_damaged_dialog(self) -> str:
                return "Mock Damaged Dialog"

            def get_encounter_dialog(self) -> str:
                return "Mock Encounter Dialog"

            def get_stat_distribution(self):
                return {
                    "health_points": 25,
                    "spell_points": 5,
                    "rigidity_points": 30,
                    "base_attack_damage": 40,
                    "base_magic_damage": 0
                }

        return MockEnemyType("MockEnemy", 1)
