from dataclasses import dataclass


@dataclass
class Stat:
    """
    Contains information to declare a statistic, like health points, magic points, etc.
    """
    name: str
    max_value: int
    value: int = -1
    is_upgradable: bool = True

    def __post_init__(self):
        if self.value == -1:
            self.reset()

    def reset(self):
        self.value = self.max_value
