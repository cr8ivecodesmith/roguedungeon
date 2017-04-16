import logging

from rogue.entities.player import Player


log = logging.getLogger('default')


def generate(gameworld):
    """Creates a player on the first room

    """
    dungeon = gameworld.current_dungeon
    player = Player(world=gameworld, dungeon=dungeon)
    log.debug('{} placed at {}'.format(player.name, (player.x, player.y)))

    gameworld.player = player
    dungeon.entities.add('player', player)
