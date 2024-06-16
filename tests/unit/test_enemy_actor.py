import pytest
from unittest.mock import MagicMock

from core.base.objects.actors.enemy import EnemyActor
from utils.dungeon_test_utils import DungeonTestUtils

# TODO: Implement these tests
# @pytest.fixture
# def setup(game_engine):
#     dungeon = DungeonTestUtils.create_test_dungeon("Test Dungeon")
#
#     room = DungeonTestUtils.create_test_rooms()[0](dungeon)
#
#     # Create a mock EnemyType with a custom stat distribution
#     # Create an EnemyType instance
#     enemy_type = DungeonTestUtils.create_test_enemy_type()
#
#     # Create an EnemyActor instance with level 5
#
#     enemy_actor = EnemyActor(
#         enemy_id="1",
#         enemy_type=enemy_type,
#     )
#
#     return enemy_actor
#
# def test_stat_distribution(setup):
#     enemy_actor = setup
#
#     # Distribute points based on the enemy's level
#     distributed_points = enemy_actor.map_stats_to_savable_dict()
#
#     # Check if the distributed points match the expected values
#     assert distributed_points["health_points"] == 40
#     assert distributed_points["spell_points"] == 5
#     assert distributed_points["rigidity_points"] == 45
#     assert distributed_points["base_attack_damage"] == 60
#     assert distributed_points["base_magic_damage"] == 5