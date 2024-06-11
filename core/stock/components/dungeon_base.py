from abc import ABC, abstractmethod

import core.stock.components.room_base as rb


class DungeonBase(ABC):
    """
    This is the base class for dungeon_pieces. All dungeon_pieces should inherit from this class. The starting room will always be
    whatever room is at (0, 0)
    """

    def __init__(self, dungeon_name: str):
        self.dungeon_name = dungeon_name
        self.rooms = {}

    @abstractmethod
    def setup_dungeon(self):
        raise NotImplementedError("Please implement the dungeon setup")

    def call_dungeon_events(self):
        pass

    def get_starting_room(self) -> 'rb.RoomBase':
        return self.rooms[(0, 0)]

    def add_room(self, room: 'rb.RoomBase'):
        self.rooms[room.room_coordinates] = room
        room.dungeon = self
