from typing import List

from statemachine import StateMachine, State


class GameStateMachine(StateMachine):
    """Handles the current state of the game"""

    def __init__(self, game_engine):
        self.manager = game_engine.game_manager
        super().__init__()

    lobby = State(initial=True)
    player_turn = State()
    enemy_turn = State()
    dungeon_event = State()

    cycle = (
            lobby.to(player_turn)
            | player_turn.to(enemy_turn)
            | enemy_turn.to(dungeon_event)
            | dungeon_event.to(player_turn)
    )

    def on_enter_lobby(self):
        self.manager.set_up_lobby()

    def on_enter_player_turn(self):
        self.manager.tick_all_player_actors()

    def on_enter_enemy_turn(self):
        self.manager.tick_all_enemy_actors()

    def on_enter_dungeon_event(self):
        self.manager.call_dungeon_events()

    def before_cycle(self, event: str, source: State, target: State, message: str = ""):
        message = ". " + message if message else ""
        return f"Switching {event} from {source.id} to {target.id}{message}"
