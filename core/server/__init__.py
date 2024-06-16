from flask_socketio import SocketIO
from flask import Flask
from core.engine import engine as e

socketio = SocketIO(async_mode='threading')
game_engine = e.Engine()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['socketio_port'] = 3232

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app, port=3232, cors_allowed_origins="*", logger=True, engineio_logger=True)

    return app
