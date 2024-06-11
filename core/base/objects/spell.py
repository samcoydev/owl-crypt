from abc import ABC, abstractmethod


class Spell(ABC):

    def __init__(self, spell_name):
        self.spell_name = spell_name

    @abstractmethod
    def cast(self):
        raise NotImplementedError("Please implement the cast method for this spell")
