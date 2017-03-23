import logging

from . import settings as st
from .bootstrap import root_console, console, tdl
from .entities import GameObject
from .map import gamemap


log = logging.getLogger('default')


def handle_keys(obj, realtime=False):
    if realtime:
        keypress = False
        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                keypress = True
        if not keypress:
            return
    else:
        user_input = tdl.event.key_wait()

    if user_input.key == 'ENTER' and user_input.alt:
        log.debug('Full screen activated!')
        tdl.set_fullscreen(True)
    elif user_input.key == 'ESCAPE':
        log.debug('Smell ya later!')
        return True

    if user_input.key == 'UP':
        obj.move(0, -1)
        log.debug('Key press UP ({}, {})'.format(obj.x, obj.y))
    if user_input.key == 'DOWN':
        obj.move(0, 1)
        log.debug('Key press DOWN ({}, {})'.format(obj.x, obj.y))
    if user_input.key == 'LEFT':
        obj.move(-1, 0)
        log.debug('Key press LEFT ({}, {})'.format(obj.x, obj.y))
    if user_input.key == 'RIGHT':
        obj.move(1, 0)
        log.debug('Key press RIGHT ({}, {})'.format(obj.x, obj.y))


def render_all(objects):
    # Draw the map first
    for y in range(st.GAME_MAP_HEIGHT):
        for x in range(st.GAME_MAP_WIDTH):
            wall = gamemap[x][y].block_sight
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

    # Draw the objects on top of the map
    for obj in objects:
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

    while not tdl.event.is_window_closed():
        # Draw the objects
        render_all(objects)
        tdl.flush()

        # Clear the previous pos of the objects
        for obj in objects:
            obj.clear()

        # Set the new player pos based on key strokes
        end_game = handle_keys(player, st.REALTIME_MOVEMENT)

        # Handle exit game
        if end_game:
            break
