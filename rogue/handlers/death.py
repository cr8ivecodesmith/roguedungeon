import logging

from rogue.handlers.status import ENTITY_STATUS
from rogue.utils import colors


log = logging.getLogger('default')


def player_death(player):
    world = player.dungeon.world

    world.message('You died!', color=colors.red)

    player.status = ENTITY_STATUS.DEAD
    player.char = '%'
    player.color = colors.dark_red


def monster_death(monster):
    world = monster.dungeon.world

    msg = '{} is dead! You gain {}xp.'.format(
        monster.name.title(),
        monster.fighter.xp
    )
    world.message(msg, colors.yellow)

    monster.status = ENTITY_STATUS.DEAD
    monster.char = '%'
    monster.color = colors.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'Remains of {}'.format(monster.name)
