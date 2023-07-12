import core.stock.components.dungeon_base as d
from core.engine.dungeon_registry import register_dungeon
import core.stock.dungeons.the_crypt.rooms as dungeon_rooms


@register_dungeon("the_crypt")
class TheCryptDungeon(d.DungeonBase):

    def __init__(self):
        super().__init__("The Crypt")

    def setup_dungeon(self):
        self.add_room(dungeon_rooms.MainTomb())
        self.add_room(dungeon_rooms.StarterRoom())
