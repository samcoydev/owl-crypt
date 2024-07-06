import copy
from unittest.mock import Mock

import pytest

from base.objects.actor import Actor
from base.objects.data_sheet import DataSheet, default_stats
from base.objects.item import Item
from stock.components.base.room_base import RoomBase


@pytest.fixture
def room():
    room = RoomBase("test_room", (0, 0))
    return room


@pytest.fixture
def two_actors(room, role):
    actors = []
    for i in range(0, 2):
        engine = Mock()
        data_sheet = DataSheet(f"data_sheet_{i}", role)
        data_sheet.set_stats(default_stats())
        actors.append(Actor(engine, room, data_sheet))
    return actors


@pytest.fixture
def item():
    return Item("Key", "test_key", "test desc")


def test_give_item_success(two_actors, item):
    actor = two_actors[0]
    actor_two = two_actors[1]
    actor.add_to_inventory(item.key, item)

    assert len(actor.inventory) == 1
    assert len(actor_two.inventory) == 0

    action = actor.give_item("test_key", actor_two.data_sheet.name)
    assert action.was_successful
    assert len(actor.inventory) == 0
    assert len(actor_two.inventory) == 1


def test_give_item_with_full_inventory(two_actors, item):
    actor = two_actors[0]
    actor_two = two_actors[1]
    item_two = Item("Filler Key", "filler_key", "filler desc")

    # Fill Actor Two inventory
    actor_two.max_inventory_size = 1
    actor_two.add_to_inventory(item_two.key, item_two)

    actor.add_to_inventory(item.key, item)

    assert len(actor.inventory) == 1
    assert len(actor_two.inventory) == 1

    action = actor.give_item(item.key, actor_two.data_sheet.name)
    assert not action.was_successful
    assert len(actor.inventory) == 1
    assert len(actor_two.inventory) == 1


def test_give_item_fail(two_actors):
    actor = two_actors[0]
    actor_two = two_actors[1]
    assert len(actor.inventory) == 0
    assert len(actor_two.inventory) == 0

    action = actor.give_item("test_key", actor_two.data_sheet.name)
    assert not action.was_successful


def test_drop_item_success(two_actors, item):
    actor = two_actors[0]
    actor.add_to_inventory(item.key, item)

    assert len(actor.current_room.artifacts) == 0

    action = actor.drop_item("test_key")
    assert action.was_successful
    assert len(actor.current_room.artifacts) == 1


def test_spend_energy_points(two_actors):
    actor = two_actors[0]
    actor.start_turn()
    assert actor.energy_points == 5
    actor.spend_energy_points("use")
    assert not actor.used_normal
    assert actor.energy_points == 4

def test_spend_energy_points_normal_first(two_actors):
    actor = two_actors[0]
    actor.start_turn()

    assert actor.data_sheet.role.name == "paladin"
    assert actor.energy_points == 5

    actor.spend_energy_points("attack")
    assert actor.used_normal
    assert actor.energy_points == 4

    actor.spend_energy_points("block")  # Assuming BLOCK is the Paladin signature
    assert actor.energy_points == 4


def test_end_turn_single_player(single_user, game_engine):
    player = single_user
    manager = game_engine.game_manager
    helper_give_item("Key", "test_key", player)

    for i in range(5):
        command_result = game_engine.command_interpreter.interpret("use test_key", player.user)
        assert command_result == PLACEHOLDER_MESSAGE
        assert player.energy_points == 4 - i

    assert player.energy_points == 0

    assert game_engine.game_state_machine.current_state.id == "enemy_turn"


def test_interact_with_entity_doorway(single_user, game_engine, dungeon):
    player = single_user
    assert game_engine.game_manager.is_players_turn(player.user.username)
    north_door = player.current_room.doorways.get("north")
    assert north_door

    result = player.interact_with_entity(north_door.entity_key)
    assert result[1]
    assert player.current_room.room_coordinates == (0, 1)

    result = player.interact_with_entity(north_door.entity_key)
    assert not result[1]
    assert player.current_room.room_coordinates == (0, 1)


def test_attack_enemy_actor(single_user, game_engine, dungeon):
    player = single_user

    # Assume no equipped item
    assert len(player.inventory) == 0
    assert game_engine.game_manager.is_players_turn(player.user.username)

    result = helper_run_command(game_engine, "interact door_north", player.user)
    # Assert it was successful
    assert result != NON_EXISTENT
    assert player.current_room.room_coordinates == (0, 1)

    enemy = player.current_room.enemies[0]
    assert enemy.current_target is not None and enemy.current_target.user.username == player.user.username

    # TODO (Attributes) - This will need to be reworked pending this
    max_hp = enemy.health_points

    # TODO (Actor vs. Actor) - Create a new set of tests to test stat changes. Rigidity points shouldn't be tested here.
    base_atk = player.base_attack_damage
    attack_result = player.attack(enemy.enemy_id)
    assert attack_result[1]

