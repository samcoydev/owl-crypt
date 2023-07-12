import core.base.objects.user as user_object
from engine.command_registry import command_registry


class CommandInterpreter:
    """Collection of commands and where they're routed"""

    def __init__(self, engine):
        self.engine = engine

    def interpret(self, command: str, user: user_object.User):
        command_parts = command.split(" ")
        command_name = command_parts[0]

        args = []
        if len(command_parts) > 1:
            args = command_parts[1:]

        if command_name not in command_registry:
            print(f"{command_name} is an unknown command")
            return "Unknown command"

        new_command = command_registry[command_name]
        if new_command.requires_args and len(args) == 0:
            return "Please provide the necessary arguments. Use HELP for more information"

        return new_command.execute(user=user, args=args)


