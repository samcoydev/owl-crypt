import os
import unittest
from unittest.mock import Mock

import engine.dungeon_registry as dungeon_registry
import core.base.objects.user as u
import core.base.objects.character as c
from engine.engine import Engine
from utils.dungeon_test_utils import DungeonTestUtils


class CommandInterpreterTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        from app import app, socketio
        # log the user in through Flask test client
        flask_test_client = app.test_client()

        # connect to Socket.IO without being logged in
        socketio_test_client = socketio.test_client(
            app, flask_test_client=flask_test_client)

        cls.game_engine = Engine(socketio_test_client)

    def setUp(self) -> None:
        # if path exists delete it
        if os.path.exists(os.path.join(os.getcwd(), "save_data", "test_interpreter_user.json")):
            os.remove(os.path.join(os.getcwd(), "save_data", "test_interpreter_user.json"))
        self.user = u.User("test_interpreter_user")
        self.game_engine.game_manager.users_in_session[self.user.socket_id] = self.user

    def test_help_command(self):
        self.result = self.game_engine.command_interpreter.interpret("help", self.user)
        self.assertNotEqual(self.result, "Unknown command")

    def test_dungeons_command(self):
        self.result = self.game_engine.command_interpreter.interpret("dungeons", self.user)
        self.assertEqual(self.result, "Dungeons:\nNo dungeons available")



    def test_lobby_command_no_users(self):
        self.game_engine.game_manager.users_in_session = {}

        self.result = self.game_engine.command_interpreter.interpret("lobby", self.user)
        self.assertEqual(self.result, "Lobby:\nNo users in lobby")

    def test_lobby_command(self):
        self.result = self.game_engine.command_interpreter.interpret("lobby", self.user)
        self.assertEqual(self.result, "Lobby:\ntest_interpreter_user - NOT READY\n")

        # "Pick" a character for the player.
        char = Mock(spec=c.Character)
        char.character_name = "Test Character"
        self.user.chosen_character = char

        ready_result = self.game_engine.command_interpreter.interpret("ready", self.user)
        self.assertEqual(ready_result, "You are now ready")

        self.result = self.game_engine.command_interpreter.interpret("lobby", self.user)
        self.assertEqual(self.result, "Lobby:\ntest_interpreter_user - Test Character - READY\n")

    def test_pick_command_no_args(self):
        self.result = self.game_engine.command_interpreter.interpret("pick", self.user)
        self.assertEqual(self.result, "Please provide the necessary arguments. Use HELP for more information")

    def test_pick_command_invalid_args(self):
        self.result = self.game_engine.command_interpreter.interpret("pick Ron The Mighty", self.user)
        self.assertEqual("You do not have a character with that name", self.result)

    def test_pick_command(self):
        self.user.create_new_character("Ron The Mighty", "paladin")
        self.result = self.game_engine.command_interpreter.interpret("pick Ron The Mighty", self.user)
        self.assertEqual("You have chosen Ron The Mighty", self.result)
        self.assertEqual(self.user.chosen_character.character_name, "Ron The Mighty")

    def test_ready_command(self):
        self.assertFalse(self.game_engine.game_manager.users_in_session[self.user.socket_id].is_ready)

        self.result = self.game_engine.command_interpreter.interpret("ready", self.user)
        self.assertEqual(self.result, "You must pick a character first")
        self.assertFalse(self.game_engine.game_manager.users_in_session[self.user.socket_id].is_ready)

        # "Pick" a character for the player.
        char = Mock(spec=c.Character)
        char.character_name = "Test Character"
        self.user.chosen_character = char

        self.result = self.game_engine.command_interpreter.interpret("ready", self.user)
        self.assertEqual(self.result, "You are now ready")
        self.assertTrue(self.game_engine.game_manager.users_in_session[self.user.socket_id].is_ready)

    def test_select_command_no_args(self):
        self.result = self.game_engine.command_interpreter.interpret("select", self.user)
        self.assertEqual(self.result, "Please provide the necessary arguments. Use HELP for more information")

    def test_select_command_invalid_args(self):
        self.result = self.game_engine.command_interpreter.interpret("select super_dungeon", self.user)
        self.assertEqual(self.result, "Please provide a valid dungeon name")

    def test_select_command_with_args(self):
        ultra_dungeon = DungeonTestUtils.create_test_dungeon("Ultra Dungeon")
        dungeon_registry.register_dungeon("ultra_dungeon")(ultra_dungeon)

        self.result = self.game_engine.command_interpreter.interpret("select ultra_dungeon", self.user)
        self.assertEqual(self.result, "Selected dungeon Ultra Dungeon")
        self.assertEqual(self.game_engine.game_manager._dungeon.dungeon_name, ultra_dungeon.dungeon_name)