import core.engine.command_interpreter as ci
import core.engine.game_manager as gm
import core.engine.game_state_machine as gsm
import core.engine.character_registry as character_registry
import core.engine.command_registry as command_registry
import core.engine.dungeon_registry as dungeon_registry


class Engine:

    def __init__(self, socketio):
        dungeon_registry.clear_registry()
        character_registry.clear_registry()
        command_registry.clear_registry()

        self.game_manager = gm.GameManager(self, socketio)
        self.game_state_machine = gsm.GameStateMachine(self)
        self.command_interpreter = ci.CommandInterpreter(self)

        import core.stock.load as stock_mod
        stock_mod.load_mod(self)
