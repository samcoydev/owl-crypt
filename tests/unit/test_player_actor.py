import pytest

from core.base.objects.item import Item, PLACEHOLDER_MESSAGE
from tests.utils.dungeon_test_utils import DungeonTestUtils
from tests.utils.user_utils import create_and_ready_users


@pytest.fixture
def test_users(dungeon, game_engine, mock_emit, persistence):
    _users = create_and_ready_users(2, game_engine.game_manager)
    game_engine.game_manager.start_game()
    player_a = _users[0].player_actor
    player_b = _users[1].player_actor
    yield player_a, player_b, game_engine


def helper_give_item(item_name, key, player):
    item = Item(item_name, item_name, "test desc")
    player.add_to_inventory(key, item)


def helper_fill_inventory(item_name, key, player):
    player.max_inventory_size = 1
    helper_give_item(item_name, key, player)


def test_give_item_success(test_users):
    player_a, player_b, game_engine = test_users
    item_name = "Key"
    target_name = player_b.character.character_name
    success_str = f"* You gave {target_name} {item_name}"

    helper_give_item(item_name, "test_key", player_a)
    assert len(player_a.inventory) == 1
    assert player_a.inventory["test_key"].name == item_name
    assert len(player_b.inventory) == 0

    result = player_a.give_item("test_key", target_name)[0]
    assert result == success_str
    assert len(player_a.inventory) == 0
    assert len(player_b.inventory) == 1
    assert player_b.inventory["test_key"].name == item_name


def test_give_item_couldnt_give(test_users):
    player_a, player_b, game_engine = test_users
    item_name = "Key"
    target_name = player_b.character.character_name
    couldnt_give_str = f"* You couldn't give {target_name} {item_name}", False

    helper_fill_inventory("Filler Key", "test_filler_key", player_b)
    helper_give_item(item_name, "test_key", player_a)

    assert len(player_a.inventory) == 1
    assert len(player_b.inventory) == 1
    assert player_b.max_inventory_size == 1

    result = player_a.give_item("test_key", target_name)
    assert result == couldnt_give_str
    assert len(player_a.inventory) == 1
    assert len(player_b.inventory) == 1


def test_give_item_fail(test_users):
    player_a, player_b, game_engine = test_users
    target_name = player_b.character.character_name
    fail_str = "You don't have that item.", False

    assert len(player_a.inventory) == 0
    assert len(player_b.inventory) == 0

    result = player_a.give_item("test_key", target_name)
    assert result == fail_str
    assert len(player_a.inventory) == 0
    assert len(player_b.inventory) == 0


def test_drop_item_success(test_users):
    player_a, player_b, game_engine = test_users
    item_name = "Key"
    success_msg = f"* You dropped __test_key__", True
    current_room = player_a.current_room

    helper_give_item(item_name, "test_key", player_a)
    assert len(current_room.artifacts) == 0

    msg = player_a.drop_item("test_key")
    assert msg == success_msg
    assert len(current_room.artifacts) == 1


def helper_test_initial_energy_and_turn_order(manager, player_a, player_b):
    assert manager.player_turn_order[0] == player_a.user.username
    assert manager.player_turn_order[1] == player_b.user.username

    assert manager.is_players_turn(player_a.user.username)
    assert not manager.is_players_turn(player_b.user.username)

    assert player_a.character.class_name == "paladin"
    assert player_a.energy_points == 5


def test_use_spends_energy(test_users, game_engine):
    player_a, player_b, game_engine = test_users
    manager = game_engine.game_manager
    helper_give_item("Key", "test_key", player_a)

    helper_test_initial_energy_and_turn_order(manager, player_a, player_b)

    command_result = game_engine.command_interpreter.interpret("use test_key", player_a.user)
    assert command_result == PLACEHOLDER_MESSAGE

    assert player_a.energy_points == 4


def test_end_turn_by_spending_all_points(test_users, game_engine):
    player_a, player_b, game_engine = test_users
    manager = game_engine.game_manager
    helper_give_item("Key", "test_key", player_a)
    helper_test_initial_energy_and_turn_order(manager, player_a, player_b)

    for i in range(5):
        command_result = game_engine.command_interpreter.interpret("use test_key", player_a.user)
        assert command_result == PLACEHOLDER_MESSAGE
        assert player_a.energy_points == 4 - i

    assert player_a.energy_points == 0
    assert manager.is_players_turn(player_b.user.username)


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