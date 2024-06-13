import core.base.types.direction_type as dr
import stock.components.base.dungeon_base as d
import core.base.objects.actors.player as pa
import stock.components.base.room_base as room_base
from base.objects.entity import Entity


class DoorwayBase(Entity):
    """A reusable class to create dungeon doorways"""

    def __init__(self, direction: 'dr.Direction', inspect_string) -> None:
        super().__init__(inspect_string)
        self.direction = direction

    def _traverse(self, player):
        """
        Traverse through the doorway

        :return tuple: (message, successful) the interaction
        """
        can_traverse = self.can_traverse(player)
        if can_traverse:
            next_room = self._get_room_on_other_side(player.current_room)
            if next_room is not None:
                player.current_room = next_room
                room_announcement = next_room.announce_player_entered_room(player)
                room_announcement_msg = f"** You move through the {self.direction.value.capitalize()} door.\n\n{room_announcement[0]}"
                return (room_announcement_msg, room_announcement[1])
            return ("You can't go that way.", False)
        return traverse_msg

    def can_traverse(self, player: 'pa.PlayerActor') -> tuple:
        """
        Override this method to add custom logic to determine if the player can traverse the doorway. You can also add
        flavor text for why the player can't traverse the doorway. By default, the player can traverse the doorway.
        """
        return ("You move through the door.", True)

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

    @property
    def is_visible(self, actor=None):
        return True

    @property
    def entity_name(self):
        return "Door"

    @property
    def entity_key(self):
        return "door_" + self.direction.value.lower()

    def interact(self, actor):
        msg = self.traverse(actor)
        return msg

