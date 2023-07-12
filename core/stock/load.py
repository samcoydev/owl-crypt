from typing import List, Type

from engine.character_registry import register_character_class
from engine.command_registry import register_command
from core.base.objects.command import Command
from core.stock.commands.vanilla_game_commands import Attack, Block, Cast, Help, Inspect, Inventory, Sneak, SpellBook, \
    Use
from core.stock.commands.vanilla_lobby_commands import Characters, Dungeons, Difficulty, Lobby, Pick, Ready, Select, \
    Upgrade
from core.stock.characters import paladin


def load_mod(engine):
    register_commands(engine)
    register_character_classes()
    register_dungeons()


def register_commands(engine):
    commands: List[Type['Command']] = [Attack, Block, Cast, Help, Inspect, Inventory, Sneak, SpellBook, Use, Characters,
                                       Dungeons, Difficulty, Lobby, Pick, Ready, Select, Upgrade]
    for command in commands:
        register_command()(command(engine))


def register_character_classes():
    character_classes = [paladin.Paladin]
    for character_class in character_classes:
        register_character_class()(character_class)


def register_dungeons():
    pass
