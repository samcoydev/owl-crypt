from dataclasses import dataclass


@dataclass
class Stat:
    """
    Contains information to declare a statistic, like health points, magic points, etc.
    """
    name: str
    value: int
    max_value: int

    def __post_init__(self):
        self.reset()

    def reset(self):
        self.value = self.max_value
