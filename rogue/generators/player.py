import logging

from rogue import settings
from rogue.entities.components.fighters import FighterComponent
from rogue.entities.generic import GameObject
from rogue.utils import colors
from rogue.handlers.death import player_death


log = logging.getLogger('default')


def generate(dungeon):
    """Creates a player on the first room

    """
    x, y = dungeon.rooms[0].center()

    fighter_component = FighterComponent(
        hp=30, defense=2, power=5,
        death_handler=player_death
    )
    player = GameObject(
        x=x, y=y,
        char='@', name='Player', color=colors.white,
        blocks=True,
        fighter=fighter_component
    )
    log.debug('{} placed at {}'.format(player.name, (player.x, player.y)))
    dungeon.entities.add('player', player)
