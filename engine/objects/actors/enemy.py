from dataclasses import dataclass

from engine import engine
from engine.objects import actor
from engine.objects.actors import player as player_actor
from dungeon_modules.base.dungeon_pieces import room_base
from dungeon_modules.base.types import enemy_type as et


@dataclass
class EnemyActor(actor.Actor):
    """A class to represent an enemy actor"""

    def __init__(self, game_engine: 'engine.Engine', enemy_type: 'et.EnemyType', enemy_id: str, health: int,
                 current_room: 'room_base.RoomBase', is_hostile: bool = True) -> None:
        super().__init__(game_engine, health, enemy_type.base_attack, current_room)
        self.enemy_id = enemy_id
        self.is_hostile = is_hostile
        self.enemy_type = enemy_type

    def kill_entity(self) -> None:
        """Removes the enemy actor from the game. Override to add flavor text"""
        print(self.enemy_type.get_death_dialog())
        self.game_engine.game_manager.remove_enemy_actor(self.enemy_id)

    def engage_player(self, player: 'player_actor.PlayerActor') -> None:
        """Sets the enemy actors target to the player """
        self.enemy_type.get_encounter_dialog()
        self.current_target = player
