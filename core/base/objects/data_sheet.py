from dataclasses import dataclass

from base.objects.stat import Stat

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
    class_name: str
    signature_command_name: str
    signature_max: int
    _command_weight_overrides = {}  # command_name - energy_cost
    signature_should_override_original_command = False
    should_append_signature_message = False  # Should the signature message appear after the original command text?

    current_actor = None
    stats_dicts: dict = None
