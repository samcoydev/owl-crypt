from abc import ABC
from dataclasses import dataclass

from typing import List


@dataclass
class ElementalType(ABC):
    name: str
    resistant_to_list: List['ElementalType']
    weak_to_list: List['ElementalType']

    def is_resistant_to(self, element: 'ElementalType') -> bool:
        if self.resistant_to_list.index(element) is not None:
            return True
        return False

    def is_weak_to(self, element: 'ElementalType') -> bool:
        if self.weak_to_list.index(element) is not None:
            return True
        return False
