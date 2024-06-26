from unittest.mock import patch

import pytest
from core.server import create_app
from core.engine.engine import Engine
from utils.dungeon_test_utils import DungeonTestUtils
from utils.user_utils import create_and_ready_users


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def game_engine(app):
    return Engine()


@pytest.fixture
def persistence():
    with patch('core.engine.data_persistence.load_data') as mock_load_data, \
            patch('os.path.join', return_value="mocked_path") as mock_join, \
            patch('builtins.open') as mock_open:
        mock_load_data.return_value = {
            "username": "",
            "pin": "",
            "characters": []
        }

        yield mock_load_data, mock_join, mock_open


@pytest.fixture
def mock_emit(app):
    with app.test_request_context('/'):
        with patch('flask_socketio.emit') as mock_emit, \
                patch('flask.request') as mock_request:

            mock_emit.return_value = None
            mock_request.namespace = "/"

            yield mock_emit, mock_request


@pytest.fixture
def dungeon(game_engine, mock_emit):
    dungeon = DungeonTestUtils.create_test_dungeon("Test Dungeon")
    game_engine.game_manager.set_dungeon(dungeon)
    dungeon.setup_dungeon(game_engine.game_manager)

    return dungeon


@pytest.fixture
def single_user(dungeon, game_engine, mock_emit, persistence):
    _user = create_and_ready_users(1, game_engine.game_manager)
    game_engine.game_manager.start_game()
    player = _user[0].player_actor
    yield player
