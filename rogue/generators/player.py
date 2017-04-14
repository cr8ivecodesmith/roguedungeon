import logging

from rogue import settings
from rogue.entities.generic import GameObject
from rogue.utils import colors


log = logging.getLogger('default')


def generate(dungeon):
    """Creates a player on the first room

    """
    player = GameObject(
        *dungeon.rooms[0].center(),
        '@', 'Player', colors.white,
        blocks=True
    )
    log.debug('{} placed at {}'.format(player.name, (player.x, player.y)))
    dungeon.entities.add('player', player)
