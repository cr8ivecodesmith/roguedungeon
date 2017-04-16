import logging

from rogue.handlers.status import ENTITY_STATUS
from rogue.utils import colors


log = logging.getLogger('default')


def player_death(player):
    player.status = ENTITY_STATUS.DEAD
    player.char = '%'
    player.color = colors.dark_red


def monster_death(monster):
    log.info('{} is dead!'.format(monster.name.title()))
    monster.status = ENTITY_STATUS.DEAD
    monster.char = '%'
    monster.color = colors.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'Remains of {}'.format(monster.name)
