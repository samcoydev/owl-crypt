import pytest

from core.engine.command_registry import command_registry
from utils.user_utils import create_test_user_and_add_to_game


@pytest.fixture(scope="module")
def user(game_engine):
    return create_test_user_and_add_to_game("test_interpreter_user", game_engine.game_manager)


def test_help(game_engine):
    result = game_engine.command_interpreter.interpret("help", user)
    assert result != "Unknown command"


def test_help_detailed(game_engine):
    result = game_engine.command_interpreter.interpret("help help", user)
    assert result == command_registry["help"].get_detailed_help_string()


def test_help_tutorial(game_engine):
    result = game_engine.command_interpreter.interpret("help tutorial", user)
    assert result == command_registry["help"].get_tutorial_str()
