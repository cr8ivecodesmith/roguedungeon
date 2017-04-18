import logging

from rogue import settings
from rogue.consoles import tdl, root_console, console
from rogue.entities.generic import GameObject
# from rogue.generators import monsters as g_mon, player as g_player
from rogue.handlers.action import player_action, monster_action
from rogue.handlers.status import GAME_STATUS, ENTITY_STATUS
from rogue.spawn import spawn_player, spawn_monsters, spawn_loot
from rogue.utils import colors
from rogue.utils.controls import get_user_input
from rogue.worlds.game import GameWorld


log = logging.getLogger('default')


def process_user_input(user_input, gameworld):
    if not user_input:
        return
    if user_input and user_input.type != 'KEYDOWN':
        return
    if user_input.key == 'ESCAPE':
        gameworld.status = GAME_STATUS.QUIT
        return

    player_action(user_input, gameworld)
    monster_action(gameworld)


def run():
    log.debug('Initializing {}'.format(settings.GAME_TITLE))

    game_state = GAME_STATUS.PLAY

    gameworld = GameWorld()
    dungeon = gameworld.generate_dungeon()

    spawn_monsters(dungeon)
    spawn_loot(dungeon)
    spawn_player(gameworld, dungeon)

    player = gameworld.player

    gameworld.message('Welcome to the dungeon stranger!', color=colors.red)

    mouse_coords = None
    gameworld.render.all(mouse_coords)

    while not tdl.event.is_window_closed():
        gameworld.render.all(mouse_coords)

        user_input = get_user_input()
        if user_input and user_input.type == 'MOUSEMOTION':
            mouse_coords = user_input.cell

        process_user_input(user_input, gameworld)

        if (
            gameworld.status == GAME_STATUS.QUIT
            or player.status == ENTITY_STATUS.DEAD
        ):
            break

    log.debug('Game closed')
