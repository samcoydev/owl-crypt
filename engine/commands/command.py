from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING
import engine.objects.user as u

if TYPE_CHECKING:
    import engine.engine as e


class Command(ABC):

    def __init__(self, game_engine):
        self.game_engine: 'e.Engine' = game_engine

    @abstractmethod
    def execute(self, user: 'u.User', args: List[str]):
        raise NotImplementedError("Please implement the execution method")

    @abstractmethod
    def get_help_string(self) -> str:
        raise NotImplementedError("Please implement a help string method")
