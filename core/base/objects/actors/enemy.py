from dataclasses import dataclass

from core.base.objects.actors import player as player_actor
from core.base.objects import actor
from core.base.types import enemy_type as et


class EnemyActor(actor.Actor):
    """
    A class to represent an enemy actor

    Would not recommend modifying at this time.
    """
    def __init__(self, game_engine, current_room, level, enemy_id, enemy_type: 'et.EnemyType', is_hostile=True):
        super().__init__(game_engine, current_room, level)
        self.enemy_id = enemy_id
        self.enemy_type = enemy_type
        self.is_hostile = is_hostile
        self.set_stats(self.enemy_type.distribute_points(level=self.level))

    def use_turn(self):
        pass

    def scale_stat_level(self, stat_value: int):
        return (stat_value * 10) * self.game_engine.game_manager.difficulty_multiplier

    def engage_player(self, player: 'player_actor.PlayerActor'):
        """Sets the enemy actors target to the player """
        self.current_target = player
        return self.enemy_type.get_encounter_dialog()

    def kill_entity(self) -> None:
        """Removes the enemy actor from the game. Override to add flavor text"""
        print(self.enemy_type.get_death_dialog())
        self.game_engine.game_manager.remove_enemy_actor(self.enemy_id)
