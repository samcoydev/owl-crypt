from typing import Dict

from flask_socketio import emit

import core.base.objects.user as u
import core.engine.engine as e

import core.base.objects.actors.enemy as enemy_actor
import core.base.objects.actors.player as player_actor
import core.stock.components.base.dungeon_base as dungeon_base
import core.engine.dungeon_registry as dungeon_registry


class GameManager:
    """Manager for game logic"""

    def __init__(self, game_engine: 'e.Engine'):
        self.game_engine = game_engine
        self._dungeon: 'dungeon_base.DungeonBase' or None = None
        self.users_in_session: Dict[str, 'u.User'] = {}  # socket_id - User
        self.player_actors: Dict[str, 'player_actor.PlayerActor'] = {}  # username - PlayerActor
        self.enemy_actors: Dict[str, 'enemy_actor.EnemyActor'] = {}  # id - EnemyActor
        self.difficulty_multiplier = 1

        # A list for keeping track of turns
        self.player_turn_order = []
        self.current_player_turn_index = 0

        self.enemy_turn_order = []
        self.current_enemy_turn_index = -1
        self.can_start_game = False
        self.game_in_session = False

    def start_game(self):
        if not self.can_start_game:
            return "Couldn't start the game.", False
        self._dungeon.setup_dungeon(game_manager=self)
        self.init_player_actors()
        self._dungeon.init_starting_room(self.get_all_player_usernames())
        self.format_player_turn_order()
        self.game_in_session = True
        self.game_engine.game_state_machine.cycle()

        self.broadcast_message(f"Turn order:\n{self.get_turn_order_string()}\n\n\n")
        self.broadcast_message(f"---=== {self.game_engine.game_manager.get_dungeon_name()} ===---\n")
        self.broadcast_message(self._dungeon.get_starting_room().view_room(first_visit=True))
        return "Game started", True

    def quick_start(self):
        self.set_dungeon(dungeon_registry.dungeon_registry.get("the_crypt"))
        for user in self.users_in_session.values():
            user.pick_character("testchar")
            self.set_user_ready(user)

        self.start_game()
        return ""

    def is_players_turn(self, username):
        """
        Check if it is the player's turn
        :param username: The username of the logged user
        :return: True if it is the player's turn, False otherwise
        """
        return self.player_turn_order[self.current_player_turn_index] == username

    def get_turn_order_string(self):
        result = ""
        for index, username in enumerate(self.player_turn_order):
            result += f"{index + 1}. {self.player_actors[username].character.character_name}\n"
        return result

    def init_player_actors(self):
        for user in self.users_in_session.values():
            self.player_actors[user.username] = player_actor.PlayerActor(self.game_engine, user, user.chosen_character,
                                                                         self._dungeon.get_starting_room())
            user.player_actor = self.player_actors[user.username]

    def format_player_turn_order(self):
        self.player_turn_order = list(self.player_actors.keys())

    def format_enemy_turn_order(self):
        self.enemy_turn_order = list(self.enemy_actors.keys())

    def begin_round_of_player_turns(self):
        self.tick_all_player_actors()
        self.current_player_turn_index = -1
        self.next_player_turn()

    def start_player_turn(self, username) -> None:
        """
        Start the player's turn and notify them
        :param username: The players username
        :return: None
        """
        actor = self.player_actors[username]
        actor.start_turn()
        self.message_player(username, "It is now your turn.")

    def next_player_turn(self):
        """
        Cycle to the next player's turn. If the last player has taken their turn, cycle the game state. The first player
        will be started in `begin_round_of_player_turns` from the state manager.
        :return: None
        """
        self.current_player_turn_index += 1

        # If the last player has just taken their turn, cycle the game state
        if self.current_player_turn_index >= len(self.player_turn_order):
            self.game_engine.game_state_machine.cycle()
        else:
            self.start_player_turn(self.player_turn_order[self.current_player_turn_index])

    def next_enemy_turn(self):
        self.current_enemy_turn_index = self.current_enemy_turn_index + 1
        if self.current_enemy_turn_index >= len(self.player_turn_order):
            self.game_engine.game_state_machine.cycle()
            self.current_enemy_turn_index = 0

    def end_game(self):
        # Level players up - The character and player should be saved from the last cycle
        for player in self.player_actors:
            self.player_actors[player].character.level_up()

        # TODO: Save data for all characters

        # TODO: Remove all player actors if saving was successful

        # Cycle game to lobby
        self.game_engine.game_state_machine.current_state = self.game_engine.game_state_machine.lobby_state
        self.game_in_session = False

    def set_up_lobby(self):
        self.unready_all_players()

    def unready_all_players(self):
        for user in self.users_in_session:
            self.users_in_session[user].is_ready = False

    def set_dungeon(self, dungeon: 'dungeon_base.DungeonBase'):
        self._dungeon = dungeon
        self.broadcast_message(f"The Dungeon has been chosen: {dungeon.dungeon_name}")
        self.unready_all_players()

    def get_dungeon_name(self):
        return self._dungeon.dungeon_name

    def call_dungeon_events(self):
        self._dungeon.call_dungeon_events()

    def save_all_character_data(self):
        for user in self.users_in_session:
            self.users_in_session[user].save_user()

    def set_user_ready(self, user: 'u.User'):
        if user.chosen_character is not None:
            self.broadcast_message(f"{user.chosen_character.character_name} is ready")
            user.is_ready = True
            self.check_start_game_conditions()
            return "You are now ready", True
        else:
            return "You must pick a character first", False

    def check_start_game_conditions(self):
        if self._dungeon is None:
            return
        all_are_ready = True
        for user in self.users_in_session:
            if not self.users_in_session[user].is_ready:
                all_are_ready = False
        if all_are_ready:
            self.can_start_game = True

    def get_user_by_sid(self, socket_id: str) -> u.User:
        return self.users_in_session.get(socket_id)

    def remove_player_actor(self, username: str):
        player = self.player_actors[username]

        print(f"Our hero {player.character.character_name} has fallen!")
        self.player_actors.pop(username)

    def get_enemy_level(self):
        # TODO - Add scaling, all that jazz
        return 1

    def add_enemy_actor(self, room, enemy_id, enemy_type, is_hostile=True):
        new_enemy = enemy_actor.EnemyActor(
            self.game_engine,
            self._dungeon.get_starting_room(),
            self.get_enemy_level(),
            enemy_id,
            enemy_type,
            is_hostile
        )
        new_enemy.current_room = room
        self.enemy_actors.update({enemy_id: new_enemy})
        return new_enemy

    def remove_enemy_actor(self, enemy_id):
        enemy = self.enemy_actors[enemy_id]

        print(f"{enemy.enemy_type.display_name} has been slain!")
        self.enemy_actors.pop(enemy_id)

    def add_user_to_session(self, socket_id: str, user: 'u.User'):
        print(user)
        user.socket_id = socket_id
        self.users_in_session.update({socket_id: user})
        print(f"{user.username} has joined the game. The current user list is: {self.users_in_session}")

    def remove_user_from_session(self, socket_id: str):
        if socket_id in self.users_in_session:
            user: u.User = self.users_in_session[socket_id]
            user.save_user()

            self.users_in_session.pop(socket_id)
            self.broadcast_message(f"{user.username} has left the game")

    def tick_all_player_actors(self):
        for player in self.player_actors:
            self.player_actors[player].tick()

    def tick_all_enemy_actors(self):
        for enemy in self.enemy_actors:
            self.enemy_actors[enemy].tick()

    def get_all_player_usernames(self):
        return list(self.player_actors.keys())

    def broadcast_to_room(self, message, room, sender_to_exclude=None):
        for player in self.player_actors:
            if self.player_actors[player].current_room == room and player != sender_to_exclude:
                self.message_player(player, message)

    def message_player(self, username, message):
        user = self.player_actors[username].user
        emit("message", {'msg': message}, to=user.socket_id)

    def broadcast_message(self, message):
        emit("message", {'msg': message})

    def get_player_in_room_by_character_name(self, room, character_name):
        for player in self.player_actors:
            if self.player_actors[player].current_room == room and self.player_actors[player].character.character_name == character_name:
                return self.player_actors[player]
