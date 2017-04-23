import logging
import os
import shelve

from rogue import settings
from rogue.consoles import tdl, root_console, console
from rogue.handlers.action import player_action, monster_action
from rogue.handlers.status import GAME_STATUS, ENTITY_STATUS
from rogue.spawn import spawn_player, spawn_monsters, spawn_loot
from rogue.utils import colors
from rogue.utils.controls import get_user_input
from rogue.worlds.game import GameWorld


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
    while not tdl.event.is_window_closed():
        console.clear()
        root_console.clear()

        choice = world.render.menu(
            '{}'.format(settings.GAME_TITLE),
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
                world.message_box('No saved game to load!')
        elif choice == 2:
            break
