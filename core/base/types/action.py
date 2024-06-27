from dataclasses import dataclass


@dataclass
class Action:
    """
    An Action is what is returned by doing something in a game world. It contains the message to give to the player, a
    flag to indicate if the action was successful or not, etc.
    """
    message: str
    was_successful: bool = True
    should_end_turn: bool = False
