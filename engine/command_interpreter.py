import engine.objects.user as user_object


class CommandInterpreter:
    """Collection of commands and where they're routed"""

    def __init__(self, engine):
        self.engine = engine

    def interpret(self, command: str, user: user_object.User):
        command_parts = command.split(" ")
        command_name = command_parts[0]

        args = []
        if len(command_parts) > 1:
            args = command_parts[:1]

        print(f"Test: {self.engine.command_registry}")
        if command_name not in self.engine.command_registry:
            print(f"{command_name} is an unknown command")
            return "Unknown command"

        new_command = self.engine.command_registry[command_name]
        if user.player_actor is None:
            return new_command.execute(user=None, args=args)
        return new_command.execute(user=user, args=args)
