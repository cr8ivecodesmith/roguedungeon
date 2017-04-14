import logging

import functools as ft

from . import settings as st
from .bootstrap import root_console, console, tdl
from .entities import GameObject
from .map import gamemap, rooms, is_visible_tile


log = logging.getLogger('default')


def get_user_input():
    """Get user input event
    Returns none on error or when there's no activity during realtime movement

    """
    user_input = None
    if st.REALTIME_MOVEMENT:
        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
    else:
        user_input = tdl.event.key_wait()
    return user_input


def move_player(obj, user_input):
    has_moved = False

    if user_input.key == 'UP':
        obj.move(0, -1)
        log.debug('Key press UP ({}, {})'.format(obj.x, obj.y))
        has_moved = True
    if user_input.key == 'DOWN':
        obj.move(0, 1)
        log.debug('Key press DOWN ({}, {})'.format(obj.x, obj.y))
        has_moved = True
    if user_input.key == 'LEFT':
        obj.move(-1, 0)
        log.debug('Key press LEFT ({}, {})'.format(obj.x, obj.y))
        has_moved = True
    if user_input.key == 'RIGHT':
        obj.move(1, 0)
        log.debug('Key press RIGHT ({}, {})'.format(obj.x, obj.y))
        has_moved = True

    return has_moved


def render_all(objects, player=None, player_moved=False, init_fov=False):
    visible_tiles = []

    # Recompute FOV if player has moved
    log.debug('Player has moved: {}'.format(player_moved))
    if player and (player_moved or init_fov):
        visible_tiles = tdl.map.quickFOV(
            player.x, player.y,
            ft.partial(is_visible_tile, gamemap),
            fov=st.FOV_ALGO,
            radius=st.FOV_TORCH_RADIUS,
            lightWalls=st.FOV_LIGHT_WALLS
        )

    # Draw the map first
    for y in range(st.GAME_MAP_HEIGHT):
        for x in range(st.GAME_MAP_WIDTH):
            visible = (x, y) in visible_tiles
            wall = gamemap[x][y].block_sight
            if not visible:
                if wall:
                    console.draw_char(
                        x, y, st.WALL_CHAR,
                        fg=st.WALL_FG_COLOR, bg=st.WALL_BG_COLOR_DARK
                    )
                else:
                    console.draw_char(
                        x, y, st.GROUND_CHAR,
                        fg=st.GROUND_FG_COLOR, bg=st.GROUND_BG_COLOR_DARK
                    )
            else:
                if wall:
                    console.draw_char(
                        x, y, st.WALL_CHAR,
                        fg=st.WALL_FG_COLOR, bg=st.WALL_BG_COLOR_LIGHT
                    )
                else:
                    console.draw_char(
                        x, y, st.GROUND_CHAR,
                        fg=st.GROUND_FG_COLOR, bg=st.GROUND_BG_COLOR_LIGHT
                    )

    # Draw the objects on top of the map
    for obj in objects:
        if (obj.x, obj.y) in visible_tiles:
            obj.draw()

    # (Blit) the console to root_console
    root_console.blit(
        console,
        0, 0,
        st.GAME_SCREEN_WIDTH, st.GAME_SCREEN_HEIGHT,
        0, 0
    )


def run():
    log.info('Game started')
    player = GameObject(
        st.GAME_SCREEN_WIDTH // 2, st.GAME_SCREEN_HEIGHT // 2,
        '@', (255, 255, 255)
    )
    npc = GameObject(
        player.x - 5, player.y,
        '@', (255, 255, 0)
    )
    objects = [
        npc,
        player,
    ]

    # Place the player at the center of the first room
    player.x, player.y = rooms[0].center()
    has_moved = False
    init_fov = True
    while not tdl.event.is_window_closed():
        # Reset user input handler
        user_input= None

        # Draw the objects
        render_all(objects, player=player,
                   player_moved=has_moved, init_fov=init_fov)
        init_fov = False  # disable initial fov computation
        tdl.flush()

        # Clear the previous pos of the objects
        for obj in objects:
            obj.clear()

        # Handle user input
        user_input = get_user_input()
        if not user_input:
            has_moved = False  # No user input means the user has not moved
            continue

        if user_input.key == 'ENTER' and user_input.alt:
            log.debug('Full screen activated!')
            tdl.set_fullscreen(True)
        elif user_input.key == 'ESCAPE':
            log.debug('Smell ya later!')
            break

        # Set the new player pos based on user_input
        has_moved = move_player(player, user_input)
