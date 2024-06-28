from unittest.mock import Mock

import pytest

from core.base.objects.data_sheet import DataSheet, default_stats
from core.engine.role_registry import register_role, role_registry, clear_registry
from core.stock.roles.paladin import Paladin


@pytest.fixture
def data_sheet():
    clear_registry()
    register_role(Paladin())
    role = role_registry["paladin"]
    data_sheet = DataSheet("data_sheet", role)
    data_sheet.set_stats(default_stats())
    data_sheet.current_actor = Mock()
    data_sheet.current_actor.session_exp_gained = 1
    return data_sheet


def test_level_up_level_increases(data_sheet):
    assert data_sheet.stats["level"].value == 1
    data_sheet.level_up()
    assert data_sheet.stats["level"].value == 2


def test_level_up_successful_action(data_sheet):
    assert data_sheet.stats["level"].value == 1
    action = data_sheet.level_up()
    assert action.was_successful


def test_level_up_successful_with_overflow_exp(data_sheet):
    assert data_sheet.stats["level"].value == 1

    # Level one will take 1 exp point. Level two will take 2 exp points.
    data_sheet.current_actor.session_exp_gained = 2
    action = data_sheet.level_up()
    assert action.was_successful


def test_level_up_unsuccessful(data_sheet):
    data_sheet.current_actor.session_exp_gained = 0
    action = data_sheet.level_up()
    assert not action.was_successful


def test_get_new_experience_requirement(data_sheet):
    assert data_sheet._get_new_experience_requirement(1) == 1
    assert data_sheet._get_new_experience_requirement(4) == 51


def test_load_saved_data(data_sheet):
    saved_data = {
        "name": "saved_sheet",
        "role": "paladin",
        "stats": {
            "level": 3,
            "health_points": 27,
            "spell_points": 3,
            "rigidity_points": 10,
            "weight_limit": 13,
            "base_attack_damage": 10,
            "base_magic_damage": 8,
            "stat_points": 3,
            "exp_gained": 2
        }
    }
    data_sheet.load_saved_data(saved_data)
    for key, val in saved_data["stats"].items():
        assert data_sheet.stats[key].value == val

    assert data_sheet.name == saved_data["name"]
    assert data_sheet.role.name == saved_data["role"]


def test_get_energy_cost_no_overrides(data_sheet):
    energy_cost = data_sheet.get_energy_cost("use")
    assert energy_cost == 1


def test_get_energy_cost_with_override(data_sheet):
    data_sheet.role.set_energy_cost_override({"use": 99})
    energy_cost = data_sheet.get_energy_cost("use")
    assert energy_cost == 99


def test_upgrade_stat(data_sheet):
    data_sheet.stats["stat_points"].value += 1
    result = data_sheet.upgrade_stat("base_attack_damage")
    assert result.was_successful
    assert data_sheet.stats["base_attack_damage"].value == 11


def test_upgrade_stat_without_stat_points(data_sheet):
    assert data_sheet.stats["stat_points"].value == 0
    result = data_sheet.upgrade_stat("spell_points")
    assert not result.was_successful


def test_upgrade_stat_with_unupgradable_stat(data_sheet):
    data_sheet.stats["stat_points"].value += 1
    result = data_sheet.upgrade_stat("level")
    assert not result.was_successful
