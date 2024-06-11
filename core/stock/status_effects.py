def fire(target_actor, damage_amount):
    """
    Applies the fire status to an actor.
    :param target_actor: The actor to apply the status to
    :param damage_amount: The amount of damage to deal
    """
    target_actor.deal_damage(damage_amount)


def bleed(target_actor, damage_amount):
    """
    Applies the bleed status to an actor.
    :param target_actor: The actor to apply the status to
    :param damage_amount: The amount of damage to deal
    """
    target_actor.deal_pure_damage(damage_amount)


def light(target_actor, healing_amount):
    """
    Applies the light status to an actor.
    :param target_actor: The actor to apply the status to
    :param healing_amount: The amount of healing per turn
    """
    target_actor.heal(healing_amount)
