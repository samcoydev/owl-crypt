from unittest.mock import patch

import pytest
from core.server import create_app
from core.engine.engine import Engine


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
def mock_emit():
    with patch('flask_socketio.emit') as mock_emit, \
            patch('flask.request') as mock_request:

        mock_emit.return_value = None
        mock_request.namespace = "/"

        yield mock_emit, mock_request
