from rogue import settings
from rogue.utils import colors


def cast_heal(caster):
    """Heal the caster

    """
    dungeon = caster.dungeon
    world = dungeon.world
    if not caster.fighter:
        return False

    if caster.fighter.hp == caster.fighter.max_hp:
        world.message(
            '{} is already in full health.'.format(caster.name),
            colors.gray
        )
        return False
    else:
        caster.fighter.heal(settings.SPELL_HEAL_AMOUNT)
        world.message(
            '{}\'s wounds feel much better.'.format(caster.name),
            colors.gray
        )
        return True
