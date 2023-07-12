from dataclasses import dataclass

from core.base.objects.actors import player as player_actor
from core.base.objects import actor
from core.base.types import enemy_type as et


@dataclass
class EnemyActor(actor.Actor):
    """
    A class to represent an enemy actor

    Would not recommend modifying at this time.
    """

    enemy_id: str
    enemy_type: 'et.EnemyType'
    is_hostile: bool = True

    def __post_init__(self):
        super().__post_init__()
        self.set_stats(self.enemy_type.distribute_points(self.level))

    def use_turn(self):
        pass

    def scale_stat_level(self, stat_value: int):
        return (stat_value * 10) * self.game_engine.game_manager.difficulty_multiplier

    def engage_player(self, player: 'player_actor.PlayerActor') -> None:
        """Sets the enemy actors target to the player """
        self.enemy_type.get_encounter_dialog()
        self.current_target = player

    def kill_entity(self) -> None:
        """Removes the enemy actor from the game. Override to add flavor text"""
        print(self.enemy_type.get_death_dialog())
        self.game_engine.game_manager.remove_enemy_actor(self.enemy_id)
