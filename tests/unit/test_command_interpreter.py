from unittest.mock import Mock

import core.engine.dungeon_registry as dungeon_registry
import core.base.objects.character as c
from utils.dungeon_test_utils import DungeonTestUtils
from utils.user_utils import create_test_user_and_add_to_game


def test_help_command(game_engine, persistence, mock_emit):
    user = create_test_user_and_add_to_game("test_interpreter_user", game_engine.game_manager)
    result = game_engine.command_interpreter.interpret("help", user)
    assert result != "Unknown command"


def test_dungeons_command(game_engine, persistence, mock_emit):
    user = create_test_user_and_add_to_game("test_interpreter_user", game_engine.game_manager)
    result = game_engine.command_interpreter.interpret("dungeons", user)
    assert result == "Dungeons:\nThe Crypt - the_crypt\n"


def test_lobby_command_no_users(game_engine, persistence, mock_emit):
    user = create_test_user_and_add_to_game("test_interpreter_user", game_engine.game_manager)
    game_engine.game_manager.users_in_session = {}

    result = game_engine.command_interpreter.interpret("lobby", user)
    assert result == "Lobby:\nNo users in lobby"


def test_lobby_command(game_engine, persistence, mock_emit):
    user = create_test_user_and_add_to_game("test_interpreter_user", game_engine.game_manager)
    result = game_engine.command_interpreter.interpret("lobby", user)
    assert result == "Lobby:\ntest_interpreter_user - NOT READY\n"

    # "Pick" a character for the player.
    char = Mock(spec=c.Character)
    char.character_name = "Test Character"
    user.chosen_character = char

    ready_result = game_engine.command_interpreter.interpret("ready", user)
    assert ready_result == "You are now ready"

    result = game_engine.command_interpreter.interpret("lobby", user)
    assert result == "Lobby:\ntest_interpreter_user - Test Character - READY\n"


def test_pick_command_no_args(game_engine, persistence, mock_emit):
    user = create_test_user_and_add_to_game("test_interpreter_user", game_engine.game_manager)
    result = game_engine.command_interpreter.interpret("pick", user)
    assert result == "Please provide the necessary arguments. Use HELP for more information"


def test_pick_command_invalid_args(game_engine, persistence, mock_emit):
    user = create_test_user_and_add_to_game("test_interpreter_user", game_engine.game_manager)
    result = game_engine.command_interpreter.interpret("pick Ron The Mighty", user)
    assert "You do not have a character with that name" == result


def test_pick_command(game_engine, persistence, mock_emit):
    user = create_test_user_and_add_to_game("test_interpreter_user", game_engine.game_manager)
    user.create_new_character("Ron The Mighty", "paladin")
    result = game_engine.command_interpreter.interpret("pick Ron The Mighty", user)
    assert "You have chosen Ron The Mighty" == result
    assert user.chosen_character.character_name == "Ron The Mighty"


def test_ready_command(game_engine, persistence, mock_emit):
    user = create_test_user_and_add_to_game("test_interpreter_user", game_engine.game_manager)
    assert not game_engine.game_manager.users_in_session[user.socket_id].is_ready

    result = game_engine.command_interpreter.interpret("ready", user)
    assert result == "You must pick a character first"
    assert not game_engine.game_manager.users_in_session[user.socket_id].is_ready

    # "Pick" a character for the player.
    char = Mock(spec=c.Character)
    char.character_name = "Test Character"
    user.chosen_character = char

    result = game_engine.command_interpreter.interpret("ready", user)
    assert result == "You are now ready"
    assert game_engine.game_manager.users_in_session[user.socket_id].is_ready


def test_select_command_no_args(game_engine, persistence, mock_emit):
    user = create_test_user_and_add_to_game("test_interpreter_user", game_engine.game_manager)
    result = game_engine.command_interpreter.interpret("select", user)
    assert result == "Please provide the necessary arguments. Use HELP for more information"


def test_select_command_invalid_args(game_engine, persistence, mock_emit):
    user = create_test_user_and_add_to_game("test_interpreter_user", game_engine.game_manager)
    result = game_engine.command_interpreter.interpret("select super_dungeon", user)
    assert result == "Please provide a valid dungeon name"


def test_select_command_with_args(game_engine, persistence, mock_emit):
    user = create_test_user_and_add_to_game("test_interpreter_user", game_engine.game_manager)
    ultra_dungeon = DungeonTestUtils.create_test_dungeon("Ultra Dungeon")
    dungeon_registry.register_dungeon(ultra_dungeon)

    result = game_engine.command_interpreter.interpret("select ultra_dungeon", user)
    assert result == "Selected dungeon Ultra Dungeon"
    assert game_engine.game_manager._dungeon.dungeon_name == ultra_dungeon.dungeon_name
