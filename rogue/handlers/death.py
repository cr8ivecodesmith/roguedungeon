import logging

from rogue.handlers.status import ENTITY_STATUS
from rogue.utils import colors


log = logging.getLogger('default')


def player_death(player):
    world = player.dungeon.world

    msg = '{} died!'.format(player.name.title())
    world.message(msg)

    player.status = ENTITY_STATUS.DEAD
    player.char = '%'
    player.color = colors.dark_red


def monster_death(monster):
    world = monster.dungeon.world

    msg = '{} is dead!'.format(monster.name.title())
    world.message(msg)

    monster.status = ENTITY_STATUS.DEAD
    monster.char = '%'
    monster.color = colors.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'Remains of {}'.format(monster.name)
