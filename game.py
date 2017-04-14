import logging

from rogue import settings
from rogue.consoles import tdl, root_console, console
from rogue.entities.generic import GameObject
from rogue.generators import monsters as g_mon, player as g_player
from rogue.handlers import game_action, player_action
from rogue.worlds.dungeon import Dungeon
from rogue.utils import colors
from rogue.utils.controls import get_user_input


log = logging.getLogger('default')


def run():
    log.debug('Initializing {}'.format(settings.GAME_TITLE))
    dungeon = Dungeon()
    g_mon.generate(dungeon)
    g_player.generate(dungeon)
    dungeon.render.compute_FOV()
    while not tdl.event.is_window_closed():
        dungeon.render.all()

        user_input = get_user_input()
        log.debug('User input: {}'.format(user_input))

        game_action.process(user_input)
        player_action.process(dungeon, user_input)

    log.debug('Game closed')
