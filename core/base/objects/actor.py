from abc import ABC, abstractmethod

from core.engine.status_registry import status_registry


class Actor(ABC):
    """
    An actor takes the abstract idea of an entity and gives it a representation in the game world. Think Players,
    Enemies, etc.

    Would not recommend modifying at this time.
    """
    def __init__(self, game_engine, current_room, level, health_points=1, spell_points=1, rigidity_points=1,
                 weight_limit=1, base_attack_damage=1, base_magic_damage=1, stat_points=0, exp_gained=0,
                 session_exp_gained=0, signature_uses=0, active_status_effects=None, current_target=None):
        self.game_engine = game_engine
        self.current_room = current_room
        self.level = level
        self.health_points = health_points
        self.spell_points = spell_points
        self.rigidity_points = rigidity_points
        self.weight_limit = weight_limit
        self.base_attack_damage = base_attack_damage
        self.base_magic_damage = base_magic_damage
        self.stat_points = stat_points
        self.exp_gained = exp_gained
        self.session_exp_gained = session_exp_gained
        self.signature_uses = signature_uses
        self.active_status_effects = active_status_effects or []
        self.current_target = current_target

    def __post_init__(self):
        self.current_target = None

    def tick(self):
        self._tick_status_effects()

    def _tick_status_effects(self):
        """
        Loops through all active status effects and applies them to the actor, while also decreasing the half-life of
        the status effect by one.

        TODO: Add a way to remove status effects from the actor
        TODO: Add a way to decrease the half-life of a status effect by a variable factor
        TODO: Add resistances to status effects
        :return: None
        """
        if self.active_status_effects is None:
            return

        for status_effect in self.active_status_effects:
            try:
                status_registry[status_effect[0]](self, status_effect[3])
                status_effect[2] -= 1
            except KeyError:
                print(f"Could not find status effect {status_effect[0]} in registry")
            if status_effect[2] <= 0:
                self.active_status_effects.remove(status_effect)

    def inflict(self, status_effect: str, duration: int, strength: int):
        """
        Inflict a status effect on the actor
        :param status_effect: The status effect to inflict
        :param duration: The duration of the status effect
        :param strength: The strength of the status effect
        :return: None
        """
        if self.active_status_effects is None:
            self.active_status_effects = []
        self.active_status_effects.append([status_effect, duration, strength])

    def deal_damage(self, damage: int):
        """
        Deal damage to health points with rigidity factored in
        """
        dmg_to_deal = damage - self.rigidity_points
        if dmg_to_deal < 0:
            dmg_to_deal = 1
        self.deal_pure_damage(dmg_to_deal)

    def deal_pure_damage(self, damage: int):
        """
        Deal damage to health points without rigidity factored in
        :param damage:
        :return:
        """
        self.set_health(self.health_points - damage)

        if self.health_points <= 0:
            self.kill_entity()

    def heal(self, heal_amount: int):
        """
        Heal the actor by a certain amount
        :param heal_amount: The amount to heal
        :return: None
        """
        self.set_health(self.health_points + heal_amount)

    def set_health(self, hp: int):
        self.health_points = hp

    def map_stats_to_savable_dict(self):
        return {
            "health_points": self.health_points,
            "spell_points": self.spell_points,
            "rigidity_points": self.rigidity_points,
            "weight_limit": self.weight_limit,
            "base_attack_damage": self.base_attack_damage,
            "base_magic_damage": self.base_magic_damage,
            "stat_points": self.stat_points,
            "exp_gained": self.exp_gained
        }

    def set_stats(self, stats_dict):
        """
        Set the stats of an actor with level and difficulty scaling.
        :param stats_dict: The stats to set
        """
        for stat_name, stat_value in stats_dict.items():
            stats_dict[stat_name] = self.scale_stat_level(stat_value)
        self._set_stats(stats_dict)

    def _set_stats(self, stats_dict):
        """
        Set the stats of an actor without scaling.
        :param stats_dict: The stats to set
        """
        self.health_points = stats_dict["health_points"]
        self.spell_points = stats_dict["spell_points"]
        self.rigidity_points = stats_dict["rigidity_points"]
        self.weight_limit = stats_dict["weight_limit"]
        self.base_attack_damage = stats_dict["base_attack_damage"]
        self.base_magic_damage = stats_dict["base_magic_damage"]
        self.stat_points = stats_dict["stat_points"]
        self.exp_gained = stats_dict["exp_gained"]

    def scale_stat_level(self, stat_value: int):
        """
        Scale a stat value based on the difficulty mode. Defaulted to "Normal"
        :param stat_value:
        :return: Scaled stat value
        """
        difficulty_multiplier = 1
        return (stat_value * 10) * difficulty_multiplier

    @abstractmethod
    def kill_entity(self) -> None:
        raise NotImplementedError("Please implement kill_entity")
