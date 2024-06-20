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
        if self.should_use_weight:
            return self.check_command_weight(user, args)

    def check_command_weight(self, user, args):
        player = user.player_actor
        if player is None:
            return "You are not in the game."

    def check_turn(self, user):
        if not self.game_engine.game_manager.is_players_turn(user.username):
            return "It's not your turn."
        return None

    @abstractmethod
    def get_help_string(self) -> str:
        raise NotImplementedError("Please implement a help string method")

    def get_detailed_help_string(self) -> str:
        return self.get_help_string()