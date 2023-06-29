from abc import ABC

import dungeon_modules.base.types.direction_type as dr
import dungeon_modules.base.dungeon_pieces.dungeon_base as d
import engine.objects.actors.player as pa
import dungeon_modules.base.dungeon_pieces.room_base as room_base


class DoorwayBase(ABC):
    """A reusable class to create dungeon doorways"""

    def __init__(self, direction: 'dr.Direction', inspect_string: str) -> None:
        self.direction = direction
        self.inspect_string = inspect_string

    def traverse(self, player: 'pa.PlayerActor') -> None:
        """Traverse through the doorway"""
        if self.can_traverse(player):
            next_room = self._get_room_on_other_side(player.current_room)
            if next_room is None:
                print("You can't go that way!")
            else:
                player.current_room = next_room
                next_room.announce_player_entered_room(player)

    def can_traverse(self, player: 'pa.PlayerActor') -> bool:
        """
        Override this method to add custom logic to determine if the player can traverse the doorway. You can also add
        flavor text for why the player can't traverse the doorway. By default, the player can traverse the doorway.
        """
        return True

    def _get_room_on_other_side(self, current_room: 'room_base.RoomBase') -> 'room_base.RoomBase':
        """Get the room on the other side of the doorway"""
        dungeon: d.DungeonBase = current_room.dungeon
        x, y = current_room.room_coordinates
        if self.direction == dr.Direction.NORTH:
            return dungeon.rooms[(x, y + 1)]
        elif self.direction == dr.Direction.SOUTH:
            return dungeon.rooms[(x, y - 1)]
        elif self.direction == dr.Direction.EAST:
            return dungeon.rooms[(x + 1, y)]
        elif self.direction == dr.Direction.WEST:
            return dungeon.rooms[(x - 1, y)]
        else:
            raise ValueError(f"Invalid direction {self.direction}")
