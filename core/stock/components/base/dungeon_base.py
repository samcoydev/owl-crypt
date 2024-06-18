from abc import ABC, abstractmethod

import core.stock.components.base.room_base as rb


class DungeonBase(ABC):
    """
    This is the base class for dungeon_pieces. All dungeon_pieces should inherit from this class. The starting room will always be
    whatever room is at (0, 0)
    """

    def __init__(self, dungeon_name: str):
        self.game_manager = None
        self.dungeon_name = dungeon_name
        self.rooms = {}

    def setup_dungeon(self, game_manager):
        self.game_manager = game_manager

    def call_dungeon_events(self):
        pass

    def init_starting_room(self, player_username_list):
        starting_room = self.rooms.get((0, 0))
        for username in player_username_list:
            starting_room.players_visited[username] = True

    def get_starting_room(self) -> 'rb.RoomBase':
        return self.rooms.get((0, 0))

    def add_room(self, room: 'rb.RoomBase'):
        self.rooms[room.room_coordinates] = room
        room.set_dungeon(self)
