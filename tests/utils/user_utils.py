from core.base.objects.user import User


def create_and_ready_users(count, game_manager):
    users = []
    for i in range(count):
        user = create_test_user_and_add_to_game(f"test_user_{i}", game_manager)
        ready_user(user, game_manager)
        users.append(user)
    return users


def create_test_user_and_add_to_game(name, game_manager):
    user = create_test_user(name)
    game_manager.add_user_to_session(name, user)
    return user


def create_test_user(name):
    user = User(name, "1111")
    user.create_new_character("test_char", "paladin")
    return user


def ready_user(user, game_manager):
    user.pick_character("test_char")
    game_manager.set_user_ready(user)


def ready_users(users, game_manager):
    for user in users:
        ready_user(user, game_manager)
