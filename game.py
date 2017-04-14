import logging

from rogue import settings
from rogue.consoles import tdl, root_console, console
from rogue.entities.generic import GameObject
from rogue.generators import monsters
from rogue.handlers import game_action, player_action
from rogue.worlds.dungeon import Dungeon
from rogue.utils import colors
from rogue.utils.controls import get_user_input


log = logging.getLogger('default')


def run():
    log.debug('Initializing {}'.format(settings.GAME_TITLE))
    dungeon = Dungeon()
    monsters.generate(dungeon)
    player = GameObject(
        0, 0,
        '@', 'Player', colors.white,
        blocks=True
    )
    player.x, player.y = dungeon.rooms[0].center()
    log.debug('{} placed at {}'.format(player.name, (player.x, player.y)))

    dungeon.entities.add('player', player)

    dungeon.render.compute_FOV()
    while not tdl.event.is_window_closed():
        dungeon.render.all()

        user_input = get_user_input()
        log.debug('User input: {}'.format(user_input))

        game_action.process(user_input)
        player_action.process(dungeon, user_input)

    log.debug('Game closed')
