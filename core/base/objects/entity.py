from abc import ABC, abstractmethod


class Entity(ABC):
    """An object that can be inspected and interacted with in the game world"""

    def __init__(self, inspect_string: str) -> None:
        self.inspect_string = inspect_string

    @property
    @abstractmethod
    def entity_name(self):
        """The name of the entity - How it is referenced in the game world"""
        raise NotImplementedError("Please implement name")

    @property
    @abstractmethod
    def entity_key(self):
        """The key of the entity - How it is referenced by command"""
        raise NotImplementedError("Please implement key")

    @property
    @abstractmethod
    def is_visible(self, actor=None):
        """Determines if the entity is visible"""
        raise NotImplementedError("Please implement is_visible")

    @abstractmethod
    def interact(self, actor=None) -> tuple:
        """
        Interact with the object

        :returns tuple: (message, should_end_turn)
        """
        raise NotImplementedError("Please implement interact")

    def inspect(self, actor=None):
        """Inspect the object override to add custom events"""
        if self.is_visible:
            return self.inspect_string
        else:
            return None
