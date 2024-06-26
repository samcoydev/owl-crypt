import pytest


@pytest.fixture
def game_state(single_user, dungeon):
    """
    Mimics the game state of a user actor and enemy actor in the same room
    """
    north_door = single_user.current_room.doorways.get("north")
    res = single_user.interact_with_entity(north_door.entity_key)
    assert res[1]

    assert len(single_user.current_room.enemies) == 1
    enemy = single_user.current_room.enemies[0]

    yield single_user, enemy

def test_deal_damage(game_state):
    player, enemy = game_state

    enemy.deal_damage()