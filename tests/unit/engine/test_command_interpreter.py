import unittest

from app import app, socketio
import engine.engine as e
import engine.objects.user as u


class CommandInterpreterTests(unittest.TestCase):

    def setUp(self) -> None:
        # log the user in through Flask test client
        flask_test_client = app.test_client()

        # connect to Socket.IO without being logged in
        socketio_test_client = socketio.test_client(
            app, flask_test_client=flask_test_client)
        self.game_engine = e.Engine(socketio_test_client)

    def test_help_command(self):
        self.user = u.User("test_interpreter_user")

        self.result = self.game_engine.command_interpreter.interpret("help", self.user)

        self.assertNotEqual(self.result, "Unknown command")
