import core.base.objects.user as user_object
from core.engine.command_registry import command_registry


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
        current_state = self.engine.game_state_machine.current_state

        if current_state == self.engine.game_state_machine.lobby:
            if new_command.command_type != "lobby" and new_command.command_type != "global":
                return "You can't do that right now"
        else:
            if new_command.command_type == "lobby":
                return "You can't do that right now"

        if new_command.requires_args and len(args) == 0:
            return "Please provide the necessary arguments. Use HELP for more information"

        execute_results = new_command.call_execute(user=user, args=args)

        self.check_to_move_next_turn(user, new_command.energy_cost())

        return execute_results

    def check_to_move_next_turn(self, user, energy_cost):
        if user.player_actor.energy_points <= 0 < energy_cost:
            self.engine.game_manager.next_player_turn()



