import unittest
from unittest.mock import MagicMock

from core.base.objects.actors.enemy import EnemyActor
from core.base.types.enemy_type import EnemyType
from engine.engine import Engine
from utils.dungeon_test_utils import DungeonTestUtils


class TestEnemyActor(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        from app import app, socketio
        # log the user in through Flask test client
        flask_test_client = app.test_client()

        # connect to Socket.IO without being logged in
        socketio_test_client = socketio.test_client(
            app, flask_test_client=flask_test_client)

        cls.game_engine = Engine(socketio_test_client)

        cls.dungeon = DungeonTestUtils.create_test_dungeon("Test Dungeon")

    def test_stat_distribution(self):
        self.room = DungeonTestUtils.create_test_rooms()[0](self.dungeon)

        # Create a mock EnemyType with a custom stat distribution
        # Create an EnemyType instance
        enemy_type = DungeonTestUtils.create_test_enemy_type()

        # Create an EnemyActor instance with level 5
        enemy_actor = EnemyActor(
            enemy_id="1",
            enemy_type=enemy_type,
            level=32,
            game_engine=self.game_engine,
            current_room=self.room,
            current_target=None
        )

        # Distribute points based on the enemy's level
        distributed_points = enemy_actor.map_stats_to_savable_dict()

        # Check if the distributed points match the expected values
        self.assertEqual(distributed_points["health_points"], 40)
        self.assertEqual(distributed_points["spell_points"], 5)
        self.assertEqual(distributed_points["rigidity_points"], 45)
        self.assertEqual(distributed_points["base_attack_damage"], 60)
        self.assertEqual(distributed_points["base_magic_damage"], 5)


if __name__ == '__main__':
    unittest.main()