from core.engine.command_registry import register_command
from core.stock.commands.vanilla_game_commands import Attack, Block, Cast, Help, Inspect, Inventory, Sneak, SpellBook, \
    Use, Interact, Drop, Give
from core.stock.commands.vanilla_lobby_commands import Characters, Dungeons, Difficulty, Lobby, Pick, Ready, Select, \
    Start, Upgrade, QuickStart
from core.stock.dungeons.the_crypt import the_crypt
from core.stock.status_effects import bleed, fire
from core.engine.dungeon_registry import register_dungeon
from core.engine.status_registry import status_registry
from engine.role_registry import register_role
from stock.roles.paladin import Paladin


def load_mod(engine):
    register_commands(engine)
    register_roles()
    register_dungeons()
    register_status_effects()


def register_commands(engine):
    game_commands = [Attack, Block, Cast, Drop, Give, Interact, Inspect, Inventory, Sneak, SpellBook, Use]
    lobby_commands = [Characters, Dungeons, Difficulty, Lobby, Pick, Ready, Select, Start, Upgrade, QuickStart]
    global_commands = [Help]

    for command in game_commands:
        register_command()(command(engine, "game"))

    for command in lobby_commands:
        register_command()(command(engine, "lobby"))

    for command in global_commands:
        register_command()(command(engine, "global"))


def register_roles():
    roles = [Paladin]
    for role in roles:
        register_role(role())


def register_dungeons():
    dungeons = [the_crypt.TheCryptDungeon]
    for dungeon in dungeons:
        register_dungeon(dungeon())


def register_status_effects():
    status_effects = [bleed, fire]
    for status_effect in status_effects:
        status_registry[status_effect.__name__] = status_effect
