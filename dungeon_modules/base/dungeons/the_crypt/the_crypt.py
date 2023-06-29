import dungeon_modules.base.dungeon_pieces.dungeon_base as d
from engine.dungeon_registry import register_dungeon
import dungeon_modules.base.dungeons.the_crypt.rooms as dungeon_rooms

@register_dungeon("the_crypt")
class TheCryptDungeon(d.DungeonBase):

    def __init__(self):
        super().__init__("The Crypt")

    def setup_dungeon(self):
        self.add_room(dungeon_rooms.MainTomb())
        self.add_room(dungeon_rooms.StarterRoom())
