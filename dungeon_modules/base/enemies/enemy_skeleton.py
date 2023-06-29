from dungeon_modules.base.types.enemy_type import EnemyType


class SkeletonEnemy(EnemyType):

    def __init__(self, name: str = "Skeleton", base_attack: int = 1):
        super().__init__(name, base_attack)

    def get_attack_dialog(self) -> str:
        return "Haha! I've got you rattled!"

    def get_damaged_dialog(self) -> str:
        return "Ouch! I've got a BONE to pick with you!"

    def get_death_dialog(self) -> str:
        return "* Bones rattle and fall to the floor *"

    def get_encounter_dialog(self) -> str:
        return "* Bones crunch and rigidly contort towards you *"
