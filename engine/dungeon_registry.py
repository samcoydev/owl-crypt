from typing import Dict
import dungeon_modules.base.dungeon_pieces.dungeon_base as dungeon

dungeon_registry: Dict[str, 'dungeon.DungeonBase'] = {}


def register_dungeon(dungeon_name: str):
    def decorator(cls: 'dungeon.DungeonBase'):
        if dungeon_name in dungeon_registry:
            raise ValueError(f"Dungeon with name '{dungeon_name}' already exists")

        dungeon_registry[dungeon_name] = cls
        print("Registered dungeon: ", dungeon_name)

        return cls

    return decorator
