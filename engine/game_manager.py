from typing import Dict

import engine.objects.user as u
import engine.engine as e

import engine.objects.actors.enemy as enemy_actor
import engine.objects.actors.player as player_actor
import dungeon_modules.base.dungeon_pieces.dungeon_base as dungeon_base


class GameManager:
    """Manager for game logic"""

    def __init__(self, game_engine: 'e.Engine', socketio):
        self.game_engine = game_engine
        self.socketio = socketio
        self._dungeon: 'dungeon_base.DungeonBase' or None = None
        self.users_in_session: Dict[str, 'u.User'] = {}  # socket_id - User
        self.player_actors: Dict[str, 'player_actor.PlayerActor'] = {}  # username - PlayerActor
        self.enemy_actors: Dict[str, 'enemy_actor.EnemyActor'] = {}  # id - EnemyActor

    def start_game(self):
        self.game_engine.game_state_machine.cycle()
        pass

    def set_up_lobby(self):
        for user in self.users_in_session:
            self.users_in_session[user].is_ready = False

    def set_dungeon(self, dungeon: 'dungeon_base.DungeonBase'):
        self._dungeon = dungeon
        self.socketio.emit("lobby_broadcast", {"message": f"The Dungeon has been chosen: {dungeon.dungeon_name}"})

    def set_user_ready(self, user: 'u.User'):
        if user.chosen_character is not None:
            self.socketio.emit("lobby_broadcast", {"message": f"{user.chosen_character.character_name} is ready"})
            user.is_ready = True
            self.check_if_all_users_are_ready()

    def check_if_all_users_are_ready(self):
        all_are_ready = True
        for user in self.users_in_session:
            if not self.users_in_session[user].is_ready:
                all_are_ready = False
        if all_are_ready:
            self.start_game()

    def get_user_by_sid(self, socket_id: str) -> u.User:
        return self.users_in_session.get(socket_id)

    def remove_player_actor(self, username: str):
        player = self.player_actors[username]

        print(f"Our hero {player.character.character_name} has fallen!")
        self.player_actors.pop(username)

    def remove_enemy_actor(self, enemy_id):
        enemy = self.enemy_actors[enemy_id]

        print(f"{enemy.enemy_type.display_name} has been slain!")
        self.enemy_actors.pop(enemy_id)

    def add_user_to_session(self, socket_id: str, username: str):
        self.users_in_session.update({socket_id: u.User(username)})
        print(f"{username} has joined the game. The current user list is: {self.users_in_session}")

    def remove_user_from_session(self, socket_id: str):
        user: u.User = self.users_in_session.get(socket_id)
        user.save_user()

        self.users_in_session.pop(socket_id)
        print(f"{user.username} has left the game. The current user list is: {self.users_in_session}")

