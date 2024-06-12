
from engine.character_registry import register_character_class
from engine.command_registry import register_command
from core.stock.commands.vanilla_game_commands import Attack, Block, Cast, Help, Inspect, Inventory, Sneak, SpellBook, \
    Use, Interact
from core.stock.commands.vanilla_lobby_commands import Characters, Dungeons, Difficulty, Lobby, Pick, Ready, Select, \
    Start, Upgrade, QuickStart
from core.stock.dungeons.the_crypt import the_crypt
from core.stock.characters import paladin
from core.stock.status_effects import bleed, fire
from engine.dungeon_registry import register_dungeon
from engine.status_registry import status_registry


def load_mod(engine):
    register_commands(engine)
    register_character_classes()
    register_dungeons()
    register_status_effects()


def register_commands(engine):
    game_commands = [Attack, Block, Cast, Interact, Inspect, Inventory, Sneak, SpellBook, Use]
    lobby_commands = [Characters, Dungeons, Difficulty, Lobby, Pick, Ready, Select, Start, Upgrade, QuickStart]
    global_commands = [Help]

    for command in game_commands:
        register_command()(command(engine, "game"))

    for command in lobby_commands:
        register_command()(command(engine, "lobby"))

    for command in global_commands:
        register_command()(command(engine, "global"))


def register_character_classes():
    character_classes = [paladin.Paladin]
    for character_class in character_classes:
        register_character_class()(character_class)


def register_dungeons():
    dungeons = [the_crypt.TheCryptDungeon]
    for dungeon in dungeons:
        register_dungeon(dungeon())


def register_status_effects():
    status_effects = [bleed, fire]
    for status_effect in status_effects:
        status_registry[status_effect.__name__] = status_effect
