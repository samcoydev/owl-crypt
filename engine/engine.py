from typing import Dict, TYPE_CHECKING, Type

if TYPE_CHECKING:
    import commands.command as cmd

import command_interpreter as ci
import game_manager as gm
import game_state_machine as gsm


class Engine:

    def __init__(self, socketio):
        self.game_manager = gm.GameManager(self, socketio)
        self.game_state_machine = gsm.GameStateMachine(self)
        self.command_interpreter = ci.CommandInterpreter(self)
        self.command_registry = {}

    def register_command(self):
        def decorator(cls: 'Type[cmd.Command]'):
            name = cls.__name__.lower()

            if name in self.command_registry:
                raise ValueError(f"Command with name '{name}' already exists")

            print("Registering command: " + name)
            self.command_registry[name] = cls(self.game_manager)

            return cls

        return decorator