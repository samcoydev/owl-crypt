from typing import Dict
import core.stock.components.dungeon_base as dungeon

dungeon_registry: Dict[str, 'dungeon.DungeonBase'] = {}


def clear_registry():
    dungeon_registry.clear()


def register_dungeon(dungeon_name: str):
    def decorator(cls: 'dungeon.DungeonBase'):
        if dungeon_name in dungeon_registry:
            raise ValueError(f"Dungeon with name '{dungeon_name}' already exists")

        dungeon_registry[dungeon_name] = cls

        return cls

    return decorator
