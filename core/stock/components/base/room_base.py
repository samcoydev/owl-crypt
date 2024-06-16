from abc import ABC, abstractmethod
from typing import List, Dict, Tuple

import core.stock.components.base.doorway_base as doorway_base
from core.base.objects.actors import enemy
from core.base.objects import artifact


class RoomBase(ABC):
    """A reusable class to create dungeon rooms"""

    def __init__(self, room_name: str, room_coordinates: Tuple[int, int]) -> None:
        """Initialize the room.
        :param room_name: The rooms name
        """
        self.room_name = room_name
        self.room_coordinates = room_coordinates
        self.enemies: List['enemy.EnemyActor'] = []
        self.artifacts: List['artifact.Artifact'] = []
        self.doorways: Dict[str, 'doorway_base.DoorwayBase'] = {}
        self.dungeon = None
        self.players_visited = {}
        self.init_doorways()

    def view_room(self, first_visit=False) -> str:
        """Displays a brief description of the room"""
        description = self.inspect_string
        if first_visit:
            description += " " + self.get_first_visit_text()
        return f"-- {self.room_name} --\n\n{description}\n\n --- \n\n {self.get_entity_strings()} \n\n"

    def get_entity_strings(self):
        val = ""
        for e in self.entities.keys():
            entity = self.entities[e]
            val += f"{entity.entity_name} - {entity.entity_key}\n"
        return val

    def parse_entity_dict(self) -> dict:
        entity_dict = {}
        for d in self.doorways:
            entity_dict[self.doorways[d].entity_key] = self.doorways[d]
        for a in self.artifacts:
            entity_dict[a.entity_key] = a
        return entity_dict

    @property
    def entities(self) -> dict:
        return self.parse_entity_dict()

    @abstractmethod
    def init_doorways(self) -> None:
        """Override this method to set up the rooms doorways"""
        raise NotImplementedError("Please implement init_doorways")

    def get_first_visit_text(self) -> str:
        """
        Override this method to return a string that will be displayed when a player enters the room for the first time
        """
        return ""

    def add_doorway(self, doorway: 'doorway_base.DoorwayBase') -> None:
        """Add a doorway to the room"""
        self.doorways[doorway.direction.value] = doorway

    def remove_artifact(self, artifact_to_remove) -> None:
        """Remove an artifact from the room"""
        self.artifacts.remove(artifact_to_remove)

    def announce_player_entered_room(self, _player):
        """
        Announce that a player has entered the room

        :param _player: The player that entered the room
        :return str: The message to display
        """
        if len(self.enemies) > 0:
            next(e for e in self.enemies if e.current_target is not None and e.is_hostile).engage_player(_player)

        if not self.players_visited.get(_player.user.username):
            msg = self.view_room(first_visit=True)
            self.players_visited[_player.user.username] = True
        else:
            msg = self.view_room()

        return msg

    def __repr__(self) -> str:
        """Return a string representation of the room."""
        return f"<Room name={self.room_name} enemies={self.enemies} artifacts={self.artifacts} room_coordinates={self.room_coordinates}>"
