import logging

from rogue import settings
from rogue.consoles import tdl, root_console, console
from rogue.entities.generic import GameObject
from rogue.generators import monsters as g_mon, player as g_player
from rogue.handlers import player_action, monster_action
from rogue.handlers.status import GAME_STATUS, ENTITY_STATUS
from rogue.worlds.game import GameWorld
from rogue.utils import colors
from rogue.utils.controls import get_user_input


log = logging.getLogger('default')


def process_user_input(user_input, gameworld):
    dungeon = gameworld.current_dungeon
    player = dungeon.entities.player

    if user_input.key == 'ESCAPE':
        gameworld.status = GAME_STATUS.QUIT

    player_action.process(user_input, gameworld)

    if (gameworld.status == GAME_STATUS.PLAY
        and player.status != ENTITY_STATUS.NO_ACTION):
        monster_action.process(dungeon)


def run():
    log.debug('Initializing {}'.format(settings.GAME_TITLE))

    game_state = GAME_STATUS.PLAY

    gameworld = GameWorld()
    dungeon = gameworld.generate_dungeon(current=True)

    g_mon.generate(dungeon)
    g_player.generate(dungeon)

    dungeon.render.compute_FOV()
    player = dungeon.entities.player
    while not tdl.event.is_window_closed():
        dungeon.render.all()

        user_input = get_user_input()
        log.debug('User input: {}'.format(user_input))

        process_user_input(user_input, gameworld)

        if (
            gameworld.status == GAME_STATUS.QUIT
            or player.status == ENTITY_STATUS.DEAD
        ):
            break

    log.debug('Game closed')
