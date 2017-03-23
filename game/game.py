import logging

from . import settings as st
from .bootstrap import root_console, console, tdl
from .entities import GameObject


log = logging.getLogger('default')


def handle_keys(pos_x, pos_y):
    user_input = tdl.event.key_wait()

    if user_input.key == 'ENTER' and user_input.alt:
        log.debug('Full screen activated!')
        tdl.set_fullscreen(True)
    elif user_input.key == 'ESCAPE':
        log.debug('Smell ya later!')
        return None, None

    if user_input.key == 'UP':
        pos_y -= 1
        log.debug('Key press UP ({}, {})'.format(pos_x, pos_y))
    if user_input.key == 'DOWN':
        pos_y += 1
        log.debug('Key press DOWN ({}, {})'.format(pos_x, pos_y))
    if user_input.key == 'LEFT':
        pos_x -= 1
        log.debug('Key press LEFT ({}, {})'.format(pos_x, pos_y))
    if user_input.key == 'RIGHT':
        pos_x += 1
        log.debug('Key press RIGHT ({}, {})'.format(pos_x, pos_y))

    return pos_x, pos_y


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
        player,
        npc
    ]

    while not tdl.event.is_window_closed():
        # Draw the objects
        for obj in objects:
            obj.draw()

        # (Blit) the console to root_console and (flush) the screen
        root_console.blit(
            console,
            0, 0,
            st.GAME_SCREEN_WIDTH, st.GAME_SCREEN_HEIGHT,
            0, 0
        )
        tdl.flush()

        # Clear the previous pos of the objects
        for obj in objects:
            obj.clear()

        # Set the new player pos based on key strokes
        player.x, player.y = handle_keys(player.x, player.y)

        # Handle exit game
        if not player.x and not player.y:
            break
