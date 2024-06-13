from typing import Dict
import stock.components.base.dungeon_base as dungeon

dungeon_registry: Dict[str, 'dungeon.DungeonBase'] = {}


def clear_registry():
    dungeon_registry.clear()


def register_dungeon(_dungeon: 'dungeon.DungeonBase'):
    name = "".join(_dungeon.dungeon_name).replace(" ", "_").lower().strip("_")

    if name in dungeon_registry:
        raise ValueError(f"Dungeon with name '{name}' already exists")

    dungeon_registry[name] = _dungeon
