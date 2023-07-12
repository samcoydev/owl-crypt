from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import core.base.objects.command as cmd

command_registry = {}


def clear_registry():
    command_registry.clear()


def register_command():
    def decorator(cls: 'cmd.Command'):
        name = cls.__class__.__name__.lower()

        if name in command_registry:
            raise ValueError(f"Command with name '{name}' already exists")

        command_registry[name] = cls

        return cls

    return decorator
