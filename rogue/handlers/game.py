import logging
import os
import shelve

from rogue import settings
from rogue.consoles import tdl, root_console, console, print_str, message_box
from rogue.handlers.action import player_action, monster_action
from rogue.handlers.status import GAME_STATUS, ENTITY_STATUS
from rogue.spawn import spawn_player, spawn_monsters, spawn_loot
from rogue.utils import colors
from rogue.utils.controls import get_user_input
from rogue.worlds.game import GameWorld

from tcod import (
    image_load,
    image_blit_2x,
)


log = logging.getLogger('default')


def new_game():
    log.debug('Initializing new game - {}'.format(settings.GAME_TITLE))

    world = GameWorld()
    dungeon = world.generate_dungeon()

    spawn_monsters(dungeon)
    spawn_loot(dungeon)
    spawn_player(world, dungeon)

    world.message('Welcome to the dungeon stranger!', color=colors.red)

    return world


def save_game(world):
    log.info('Saving game...')
    save = shelve.open(os.path.join(
        settings.DATADIR,
        'savegame'
    ), 'n')
    save['world'] = world
    save.close()
    log.info('Saved!')
    return


def load_game():
    log.info('Loading game...')
    load = shelve.open(os.path.join(
        settings.DATADIR,
        'savegame'
    ), 'r')
    world = load['world']
    load.close()
    log.info('Loaded!')
    return world


def play_game(world):
    player = world.player
    mouse_coords = None
    world.render.all(mouse_coords)

    while not tdl.event.is_window_closed():
        world.render.all(mouse_coords)

        user_input = get_user_input()

        if user_input and 'MOUSE' in user_input.type:
            mouse_coords = user_input.cell
            continue

        if user_input and user_input.key == 'ESCAPE':
            world.status = GAME_STATUS.QUIT

        if user_input and user_input.type == 'KEYDOWN':
            player_action(user_input, world)
            monster_action(world)

        if (
            world.status == GAME_STATUS.QUIT or
            player.status == ENTITY_STATUS.DEAD
        ):
            save_game(world)
            break

    log.debug('Game closed')
    return


def main_menu():
    world = GameWorld()
    bg_image = image_load(settings.MAIN_MENU_BG_IMG)

    while not tdl.event.is_window_closed():
        console.clear()
        root_console.clear()

        image_blit_2x(bg_image, 0, 0, 0)

        print_str(
            settings.GAME_SCREEN_WIDTH / 2 - (len(settings.GAME_TITLE) / 2),
            settings.GAME_SCREEN_HEIGHT / 2 - 4,
            settings.GAME_TITLE.upper(),
            bg=None, fg=colors.gold,
            bg_alpha=0.75
        )
        print_str(
            settings.GAME_SCREEN_WIDTH / 2 - (len(settings.GAME_AUTHOR) / 2),
            settings.GAME_SCREEN_HEIGHT - 3,
            settings.GAME_AUTHOR,
            bg=None, fg=colors.gold,
            bg_alpha=0.75
        )

        choice = world.render.menu(
            '',
            [
                'Play a new game',
                'Continue last game',
                'Quit',
            ],
            24
        )

        world.render.flush_console()

        if choice == 0:
            new_world = new_game()
            play_game(new_world)
        elif choice == 1:
            try:
                old_world = load_game()
                old_world.status = GAME_STATUS.PLAY
                play_game(old_world)
            except Exception as err:
                log.warn(err)
                msg = 'No saved game to load!'
                message_box(
                    settings.GAME_SCREEN_WIDTH / 2 - (len(msg) / 2),
                    settings.GAME_SCREEN_HEIGHT / 2,
                    msg,
                    width=len(msg),
                    fg=colors.red,
                    bg_alpha=1.0
                )
        elif choice == 2:
            break
