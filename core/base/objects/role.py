from dataclasses import dataclass


@dataclass
class Role:
    """
    A Role is also referred to as a Class in other RPGs. This is where you will define roles like Paladin, Rogue, etc.

    This is also the default role that has no special abilities or signatures.
    """
    name: str
    signature_command_name: str
    signature_max: int
    _command_weight_overrides = {}  # command_name - energy_cost
    signature_should_override_original_command = False
    should_append_signature_message = False  # Should the signature message appear after the original command text?