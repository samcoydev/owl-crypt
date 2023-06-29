from dataclasses import dataclass
from typing import TYPE_CHECKING

from engine.objects.actor import Actor

if TYPE_CHECKING:
    from dungeon_modules.base.dungeon_pieces.room_base import RoomBase
    from engine.objects.characters.character import Character
    from engine.objects.user import User
    import engine.engine as e


@dataclass
class PlayerActor(Actor):
    """A class to represent a player actor"""

    def __init__(self, game_engine: 'e.Engine', user: 'User', character: 'Character', health: int, damage: int,
                 current_room: 'RoomBase') -> None:
        super().__init__(game_engine, health, damage, current_room)
        self.user = user
        self.character = character

    def set_health(self, hp: int):
        super().set_health(hp)
        self.character.set_health(hp)

    def view_surroundings(self) -> None:
        """Prompt to view the players surroundings"""
        self.current_room.view_room()

    def interact_with_artifact(self, artifact_name: str) -> None:
        """Prompt to interact with an artifact by name in the players current room"""
        self.current_room.find_artifact_by_name(artifact_name).interact(self)

    def inspect_artifact(self, artifact_name: str) -> None:
        """Prompt to inspect an artifact by name in the players current room"""
        self.current_room.find_artifact_by_name(artifact_name).inspect(self)

    def kill_entity(self) -> None:
        self.game_engine.game_manager.remove_player_actor(self.user.username)
