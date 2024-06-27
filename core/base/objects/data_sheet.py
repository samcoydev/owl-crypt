from dataclasses import dataclass
from typing import TYPE_CHECKING
from base.objects.stat import Stat

if TYPE_CHECKING:
    from base.objects.role import Role

DEFAULT_STATS = {
    "health_points": Stat("Health Points", 10, 10),
    "spell_points": Stat("Spell Points", 10, 10),
    "rigidity_points": Stat("Rigidity Points", 10, 10),
    "weight_limit": Stat("Weight Limit", 10, 10),
    "base_attack_damage": Stat("Base Attack Damage", 10, 10),
    "base_magic_damage": Stat("Base Magic Damage", 10, 10),
    "stat_points": Stat("Stat Points", 10, 10),
    "exp_gained": Stat("Experience Points", 10, 10),
}


@dataclass
class DataSheet:
    """
    A container representing something akin to a table-top RPG character sheet. This contains the statistics
    for a controllable object, or actor.
    """
    name: str
    role: 'Role'
    current_actor = None
    stats_dicts: dict = None
