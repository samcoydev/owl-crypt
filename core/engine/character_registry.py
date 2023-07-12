from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

class_registry = {}


def clear_registry():
    class_registry.clear()


def register_character_class():
    def decorator(cls):
        name = cls.__name__.lower()

        if name in class_registry:
            raise ValueError(f"Class with name '{name}' already exists")

        class_registry[name] = cls

        return cls

    return decorator
