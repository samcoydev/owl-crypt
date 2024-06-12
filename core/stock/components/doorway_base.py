from abc import ABC

import core.base.types.direction_type as dr
import core.stock.components.dungeon_base as d
import core.base.objects.actors.player as pa
import core.stock.components.room_base as room_base
from base.objects.entity import Entity


class DoorwayBase(Entity):
    """A reusable class to create dungeon doorways"""

    def __init__(self, direction: 'dr.Direction', inspect_string) -> None:
        super().__init__(inspect_string)
        self.direction = direction

    def traverse(self, player: 'pa.PlayerActor'):
        """Traverse through the doorway"""
        if self.can_traverse(player):
            next_room = self._get_room_on_other_side(player.current_room)
            if next_room is not None:
                player.current_room = next_room
                room_announcement = next_room.announce_player_entered_room(player)
                room_announcement_msg = f"** You move through the {self.direction.value.capitalize()} door.\n\n{room_announcement[0]}"
                return (room_announcement_msg, room_announcement[1])
        return False

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

    # Entity Methods
    def is_visible(self, player):
        return True

    def entity_name(self):
        return "Door"

    def entity_key(self):
        return "door_" + self.direction.value.lower()

    def interact(self, actor):
        response = self.traverse(actor)
        if response is False:
            return ("You can't go that way.", False)
        return response

