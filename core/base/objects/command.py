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

    @abstractmethod
    def execute(self, user: 'u.User', args: List[str]):
        raise NotImplementedError("Please implement the execution method")

    @abstractmethod
    def get_help_string(self) -> str:
        raise NotImplementedError("Please implement a help string method")
