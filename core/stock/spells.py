def fireball(caster, target):
    """
    Casts a fireball spell at a target.
    :param caster:
    :param target:
    :return:
    """
    target.deal_damage(caster.get_magic_damage())
    target.inflict("fire", 3, 2)


def heal(caster, target):
    """
    Casts a heal spell at a target.
    :param caster:
    :param target:
    :return:
    """
    if target is None:
        target = caster
    target.heal(10)


def orb_of_light(caster, target):
    """
    Casts an orb of light spell at a target.
    :param caster:
    :param target:
    :return:
    """
    if target is None:
        target = caster
    target.inflict("light", 5, 2)
