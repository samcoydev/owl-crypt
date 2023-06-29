from flask_socketio import SocketIO
from flask import Flask, request
from flask_socketio import emit
import engine.engine as e

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
socketio = SocketIO(app, port=3232, cors_allowed_origins="http://localhost:3000", logger=True, engineio_logger=True)

game_engine = e.Engine(socketio)


@socketio.on('connect')
def on_connect():
    """Get the socket ID on event connect and attach a username."""
    print("Someone connected")


@socketio.on('disconnect')
def disconnect():
    """Sent by clients when they leave the game"""
    print("Someone disconnected")
    game_engine.game_manager.remove_user_from_session(request.sid)


@socketio.on('command')
def receive_command(command: str):
    print("Someone sent a command")
    game_engine.command_interpreter.interpret(command, game_engine.game_manager.get_user_by_sid(request.sid))


@socketio.on('join_game')
def on_join_game(data):
    print(f"On join game {data}")
    if (data["username"] or request.sid) is None:
        raise ConnectionRefusedError('Missing a username!')

    game_engine.game_manager.add_user_to_session(request.sid, data["username"])

    emit('user_joined_game', {'msg': f"{data['username']} has joined the game!"})


@socketio.on('ready')
def set_ready():
    print(f"Player ready")
    user = game_engine.game_manager.get_user_by_sid(request.sid)
    game_engine.game_manager.set_user_ready(user)
    if user.is_ready:
        emit('user_ready', {'msg': f"{user.username} is now ready."})
    else:
        emit('user_ready', {'msg': f"{user.username} is no longer ready."})


if __name__ == '__main__':
    socketio.run(app)
