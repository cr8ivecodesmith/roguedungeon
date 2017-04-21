from rogue import settings
from rogue.utils import colors

from rogue.entities.components.monsters import ConfusedMonsterAIComponent


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


def cast_lightning(caster):
    """Cast lightning on the closest monster from the player

    """
    dungeon = caster.dungeon
    world = dungeon.world
    if not caster.fighter:
        return False

    target = caster.closest_monster(settings.SPELL_LIGHTNING_RANGE)
    if not target:
        world.message('No enemy is close enough to strike.', colors.red)
        return False

    world.message(
        'A lightning bolt strikes the {} with a loud thunder! The damage '
        'is {} hit points.'.format(
            target.name, settings.SPELL_LIGHTNING_DAMAGE
        ), colors.orange
    )
    target.fighter.take_damage(settings.SPELL_LIGHTNING_DAMAGE)
    return True


def cast_confuse(caster):
    """Cast confusion to a targeted monster in FOV

    """
    dungeon = caster.dungeon
    world = dungeon.world

    world.message(
        'Left-click an enemy to confuse it, or right-click to cancel.',
        colors.light_cyan,
        force_render=True
    )
    target = caster.target_monster(settings.SPELL_CONFUSE_RANGE)
    if not target:
        return False

    confused_ai = ConfusedMonsterAIComponent(old_ai=target.ai)
    confused_ai.owner = target
    target.ai = confused_ai

    world.message(
        'The eyes of the {} look vacant as it starts to stumble '
        'around!'.format(target.name), colors.light_green
    )
    return True


def cast_fireball(caster):
    """Cast a fireball to a targeted tile in FOV and burn all monsters
    including the player.

    """
    dungeon = caster.dungeon
    world = dungeon.world
    monsters = dungeon.entities.monsters

    world.message(
        'Left-click a target tile for the fireball, or right-click to '
        'cancel.', colors.light_cyan,
        force_render=True
    )

    x, y = caster.target_tile()
    if x is None:
        return False

    world.message(
        'The fireball explodes, burning everything within {} '
        'tiles!'.format(settings.SPELL_FIREBALL_RADIUS), colors.orange,
        force_render=True
    )

    for obj in monsters:
        valid = (
            obj.distance(x, y) <= settings.SPELL_FIREBALL_RADIUS and
            obj.fighter
        )
        if valid:
            world.message(
                'The {} gets burned for {} hit points.'.format(
                    obj.name, settings.SPELL_FIREBALL_DAMAGE
                ), colors.orange
            )
            obj.fighter.take_damage(settings.SPELL_FIREBALL_DAMAGE)
    return True
