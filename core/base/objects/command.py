from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING
import core.base.objects.user as u

if TYPE_CHECKING:
    from core.engine import engine as e


class Command(ABC):

    def __init__(self, game_engine, command_type: str = "global", requires_args: bool = False):
        self.game_engine: 'e.Engine' = game_engine
        self.requires_args = requires_args
        self.command_type = command_type

    def execute(self, user: 'u.User', args: List[str]):
        pass

    def call_execute(self, user: 'u.User', args: List[str]):
        """
        Execute a command. Spend energy points on successful actions, and
        call signature commands based on the executing player.
        :param user: The user entering the command
        :param args: Any arguments for the command
        :return: Flavor text resulting from the action
        """
        if user.player_actor:
            if self.is_turn_session_based and not self._is_players_turn(user):
                return "It isn't your turn."

            if not user.player_actor.can_afford_energy_cost(self.get_name()):
                return "You don't have enough energy to do that."

            if self._is_calling_signature(user):
                response = self._call_signature(user, args)
            else:
                response = self.execute(user, args)

            # Only spend points if the action was successful
            if response[1]:
                user.player_actor.spend_energy_points(self.get_name())

            # Just get the message
            response = response[0]
        else:
            response = self.execute(user, args)

        return response

    def _call_signature(self, user, args) -> str:
        character = user.player_actor.character
        signature_effect_response = character.signature_effect(args)

        # Only continue executing if the signature doesn't override the usual
        # execution, and if the signature was successful.
        if character.signature_should_override_original_command or not signature_effect_response[1]:
            return signature_effect_response

        execute_response = self.execute(user, args)
        return self._compose_execute_message(character, execute_response, signature_effect_response)

    @staticmethod
    def _compose_execute_message(character, execute_response, signature_effect_response):
        if character.should_append_signature_message:
            return execute_response + "\n" + signature_effect_response

        return signature_effect_response + "\n" + execute_response

    def _is_calling_signature(self, user):
        return user.player_actor.character.signature_command_name == self.get_name()

    def _is_players_turn(self, user):
        return self.game_engine.game_manager.is_players_turn(user.username)

    def get_name(self) -> str:
        return self.__class__.__name__.lower()

    @property
    def is_turn_session_based(self):
        return False

    @property
    def energy_cost(self):
        return 0

    @abstractmethod
    def get_help_string(self) -> str:
        raise NotImplementedError("Please implement a help string method")

    def get_detailed_help_string(self) -> str:
        return self.get_help_string()
