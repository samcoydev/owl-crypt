from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from base.objects.data_sheet import DataSheet


@dataclass
class NpcBehaviourBase:
    """
    A base class used to define the behaviour of an NPC.
    """
    data_sheet: 'DataSheet'
