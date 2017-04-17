import logging

from rogue.entities.player import Player


log = logging.getLogger('default')


def generate(gameworld, dungeon):
    """Initializes the player on the first room

    """
    player = Player(world=gameworld)
    gameworld.player = player
    player.dungeon = dungeon
    player.x, player.y = dungeon.rooms[0].center()

    log.debug('{} placed at {}'.format(player.name, (player.x, player.y)))
