from abc import ABC


class ClassType(ABC):

    def __init__(self, display_name: str, name: str, signature_command, signature_max: int):
        self.display_name = display_name
        self.name = name
        self.signature_command = None
        self.signature_max = signature_max

    def get_inspect_effect(self):
        return None

    def get_block_effect(self):
        return None

    def get_cast_effect(self):
        return None

    def get_attack_effect(self):
        return None

    def get_sneak_effect(self):
        return None
