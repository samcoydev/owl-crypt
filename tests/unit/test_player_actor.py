import unittest
from unittest.mock import Mock, patch

from flask import Flask
from flask_socketio import SocketIO

from core.base.objects.item import Item
from core.engine.engine import Engine
from tests.utils.dungeon_test_utils import DungeonTestUtils
from tests.utils.user_utils import create_and_ready_users


class PlayerActorTest(unittest.TestCase):

    @classmethod
    @patch('flask_socketio.emit')
    def setUpClass(cls, mock_emit) -> None:
        mock_socket_io = Mock()
        cls.game_engine = Engine()

    @patch('flask_socketio.emit')
    def setUp(self, mock_emit) -> None:
        self.mock_emit = mock_emit
        self.mock_emit.return_value = None

        self.manager = self.game_engine.game_manager

        self.dungeon = DungeonTestUtils.create_test_dungeon("Test Dungeon")
        self.dungeon.setup_dungeon()
        self.manager.set_dungeon(self.dungeon)

        self._users = create_and_ready_users(2, self.manager)
        self.user_a = self._users[0]
        self.user_b = self._users[1]
        self.player_a = self.user_a.player_actor
        self.player_b = self.user_b.player_actor

    def helper_give_item(self, item_name, key, player):
        item = Item(item_name, item_name, "test desc")
        player.add_to_inventory(key, item)

    def helper_fill_inventory(self, item_name, key, player):
        player.max_inventory_size = 1
        self.helper_give_item(item_name, key, player)

    def test_give_item_success(self):
        item_name = "Key"
        target_name = self.player_b.character.character_name
        success_str = f"* You gave {target_name} {item_name}"

        self.helper_give_item(item_name, "test_key", self.player_a)
        self.assertEqual(len(self.player_a.inventory), 1)
        self.assertEqual(self.player_a.inventory["test_key"].name, item_name)
        self.assertEqual(len(self.player_b.inventory), 0)

        result = self.player_a.give_item("test_key", target_name)
        self.assertEqual(result, success_str)
        self.assertEqual(len(self.player_a.inventory), 0)
        self.assertEqual(len(self.player_b.inventory), 1)
        self.assertEqual(self.player_b.inventory["test_key"].name, item_name)

    def test_give_item_couldnt_give(self):
        item_name = "Key"
        target_name = self.player_b.character.character_name
        couldnt_give_str = f"* You couldn't give {target_name} {item_name}"

        self.helper_fill_inventory("Filler Key", "test_filler_key", self.player_b)
        self.helper_give_item(item_name, "test_key", self.player_a)

        self.assertEqual(len(self.player_a.inventory), 1)
        self.assertEqual(len(self.player_b.inventory), 1)
        self.assertEqual(self.player_b.max_inventory_size, 1)

        result = self.player_a.give_item("test_key", target_name)
        self.assertEqual(result, couldnt_give_str)
        self.assertEqual(len(self.player_a.inventory), 1)
        self.assertEqual(len(self.player_b.inventory), 1)

    def test_give_item_fail(self):
        target_name = self.player_b.character.character_name
        fail_str = "You don't have that item."

        self.assertEqual(len(self.player_a.inventory), 0)
        self.assertEqual(len(self.player_b.inventory), 0)

        result = self.player_a.give_item("test_key", target_name)
        self.assertEqual(result, fail_str)
        self.assertEqual(len(self.player_a.inventory), 0)
        self.assertEqual(len(self.player_b.inventory), 0)


if __name__ == '__main__':
    unittest.main()
