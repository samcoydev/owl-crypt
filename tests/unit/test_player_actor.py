import pytest

from core.base.objects.item import Item
from tests.utils.dungeon_test_utils import DungeonTestUtils
from tests.utils.user_utils import create_and_ready_users


@pytest.fixture
def dungeon(game_engine, mock_emit):
    dungeon = DungeonTestUtils.create_test_dungeon("Test Dungeon")
    dungeon.setup_dungeon()
    game_engine.game_manager.set_dungeon(dungeon)

    return dungeon


@pytest.fixture
def test_users(dungeon, game_engine, mock_emit, persistence):
    _users = create_and_ready_users(2, game_engine.game_manager)
    game_engine.game_manager.start_game()
    print(_users)
    player_a = _users[0].player_actor
    player_b = _users[1].player_actor
    yield player_a, player_b


def helper_give_item(item_name, key, player):
    item = Item(item_name, item_name, "test desc")
    player.add_to_inventory(key, item)


def helper_fill_inventory(item_name, key, player):
    player.max_inventory_size = 1
    helper_give_item(item_name, key, player)


def test_give_item_success(test_users):
    player_a, player_b = test_users
    item_name = "Key"
    target_name = player_b.character.character_name
    success_str = f"* You gave {target_name} {item_name}"

    helper_give_item(item_name, "test_key", player_a)
    assert len(player_a.inventory) == 1
    assert player_a.inventory["test_key"].name == item_name
    assert len(player_b.inventory) == 0

    result = player_a.give_item("test_key", target_name)
    assert result == success_str
    assert len(player_a.inventory) == 0
    assert len(player_b.inventory) == 1
    assert player_b.inventory["test_key"].name == item_name


def test_give_item_couldnt_give(test_users):
    player_a, player_b = test_users
    item_name = "Key"
    target_name = player_b.character.character_name
    couldnt_give_str = f"* You couldn't give {target_name} {item_name}"

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
    player_a, player_b = test_users
    target_name = player_b.character.character_name
    fail_str = "You don't have that item."

    assert len(player_a.inventory) == 0
    assert len(player_b.inventory) == 0

    result = player_a.give_item("test_key", target_name)
    assert result == fail_str
    assert len(player_a.inventory) == 0
    assert len(player_b.inventory) == 0
