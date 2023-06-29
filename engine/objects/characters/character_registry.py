from typing import Dict, TYPE_CHECKING, Type

if TYPE_CHECKING:
    from engine.objects.characters.character import Character

class_registry = {}


def register_character_class():
    def decorator(cls):
        name = cls.__name__.lower()

        if name in class_registry:
            raise ValueError(f"Class with name '{name}' already exists")

        class_registry[name] = cls

        return cls

    return decorator
