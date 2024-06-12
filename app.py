from flask_socketio import SocketIO
from flask import Flask, request, render_template, flash
from flask_socketio import emit
from core.engine import engine as e
import core.base.objects.user as u

from engine.data_persistence import load_data

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['socketio_port'] = 3232

socketio = SocketIO(app, port=3232, cors_allowed_origins="*", logger=True, engineio_logger=True)

game_engine = None


def load_user(username):
    user_dict = load_data(username)
    print("Username: ", username, user_dict)
    if len(user_dict) > 0:
        user = u.User(user_dict["username"], user_dict["pin"])
        print("Load User: ", user)
        return user

    return None


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('create-account-attempt')
def register(data):
    username = data['username']
    pin = data['pin']

    if len(username) < 1 or len(pin) < 1:
        return 'Username and PIN must be at least 1 character long. Please try again.'

    print("Registering user: " + username + " with PIN: " + pin)

    user = load_user(username)
    print(user)
    if user is not None:
        print('Username already exists. Please try again.')
        return render_template('login.html')

    user = u.User(username, pin)
    user.save_user()

    print(user.is_active, user.username)


@socketio.on('login-attempt')
def login(data):
    username = data['username']
    pin = data['pin']

    user = load_user(username)
    if user and user.pin == pin:
        emit('login-success')
        if not game_engine.game_manager.game_in_session:
            print(f"User {user.username} connected")
            game_engine.game_manager.add_user_to_session(request.sid, user)
            broadcast_message(f"{user.username} has joined the game!")
        else:
            emit('login-error', 'Failed to login user. Please try again.')
    else:
        emit('login-error', 'Invalid username or PIN. Please try again.')


@socketio.on('connect')
def on_connect(auth):
    """Get the socket ID on event connect and attach a username."""
    # user = current_user
    # if user.is_anonymous:
    #     print("Is anon: ", user)
    #     return False
    #
    # print(f"Current user: {user}")
    # if user.is_authenticated:
    #     if not game_engine.game_manager.game_in_session:
    #         print(f"User {user.username} connected")
    #         game_engine.game_manager.add_user_to_session(request.sid, user)
    #         broadcast_message(f"{user.username} has joined the game!")
    #     else:
    #         flash('The game is currently in session. Please try again when the game is over.')
    #         redirect(url_for('login'))
    # else:
    #     print("Someone connected without logging in")
    #     flash('Unauthorized. Please log in and try again.')
    #     logout_user()
    #     redirect(url_for('login'))


@socketio.on('disconnect')
def disconnect():
    """Sent by clients when they leave the game"""
    print("Someone disconnected")
    # TODO: Possible bug if user connects, gets a connection refused error, and then disconnects. The value wont be in
    #  the dict
    game_engine.game_manager.remove_user_from_session(request.sid)


@socketio.on('command')
def receive_command(command: str):
    result = game_engine.command_interpreter.interpret(command, game_engine.game_manager.get_user_by_sid(request.sid))
    emit('message', {'msg': result}, to=request.sid)


@socketio.on('join_game')
def on_join_game(data):
    print(f"On join game {data}")
    if (data["username"] or request.sid) is None:
        flash('Missing a username!')

    # game_engine.game_manager.add_user_to_session(request.sid, data["username"])


@socketio.on('ready')
def set_ready():
    print(f"Player ready")
    user = game_engine.game_manager.get_user_by_sid(request.sid)
    game_engine.game_manager.set_user_ready(user)
    if user.is_ready:
        broadcast_message(f"{user.username} is now ready")
    else:
        broadcast_message(f"{user.username} is no longer ready")


def broadcast_message(message):
    emit("message", {'msg': message}, broadcast=True)


if __name__ == 'app':
    print("Starting Server")
    socketio.run(app, port=3232, allow_unsafe_werkzeug=True)
    game_engine = e.Engine(socketio)
