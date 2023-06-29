from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Dict, Tuple

import dungeon_modules.base.dungeon_pieces.doorway_base as doorway_base
import dungeon_modules.base.dungeon_pieces.dungeon_base as dungeon_base
from engine.objects.actors import enemy
from engine.objects.actors import player
from engine.objects import artifact


class RoomBase(ABC):
    """A reusable class to create dungeon rooms"""

    def __init__(self, room_name: str, room_coordinates: Tuple[int, int], dungeon: 'dungeon_base.DungeonBase') -> None:
        """Initialize the room.
        :param room_name: The rooms name
        """
        self.room_name = room_name
        self.room_coordinates = room_coordinates
        self.enemies: List['enemy.EnemyActor'] = []
        self.artifacts: List['artifact.Artifact'] = []
        self.doorways: Dict[str, 'doorway_base.DoorwayBase'] = {}
        self.dungeon = dungeon
        self.init_doorways()

    @abstractmethod
    def view_room(self):
        """Displays a brief description of the room"""
        raise NotImplementedError("Please implement view_room")

    @abstractmethod
    def init_doorways(self) -> None:
        """Override this method to set up the rooms doorways"""
        raise NotImplementedError("Please implement init_doorways")

    def add_doorway(self, doorway: 'doorway_base.DoorwayBase') -> None:
        """Add a doorway to the room"""
        self.doorways[doorway.direction.value] = doorway

    def announce_player_entered_room(self, _player: 'player.PlayerActor') -> None:
        if len(self.enemies) > 0:
            self.view_room()
            next(e for e in self.enemies if e.current_target is not None and e.is_hostile).engage_player(_player)

    def find_artifact_by_name(self, artifact_name: str) -> 'artifact.Artifact':
        """Find an artifact by name"""
        return next(a for a in self.artifacts if a.artifact_name == artifact_name)

    def __repr__(self) -> str:
        """Return a string representation of the room."""
        return f"<Room name={self.room_name} enemies={self.enemies} artifacts={self.artifacts}>"
