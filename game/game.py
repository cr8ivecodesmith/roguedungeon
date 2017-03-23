import logging

from . import settings as st
from .bootstrap import console, tdl


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
    player_x, player_y = st.GAME_SCREEN_WIDTH // 2, st.GAME_SCREEN_HEIGHT // 2

    while not tdl.event.is_window_closed():
        # Draw the character
        console.draw_char(player_x, player_y, '@', bg=None, fg=(255, 255, 255))
        tdl.flush()

        # Clear the previous pos of the character
        console.draw_char(player_x, player_y, ' ', bg=None)

        # Set the new player pos based on key strokes
        player_x, player_y = handle_keys(player_x, player_y)

        # Handle exit game
        if not player_x and not player_y:
            break
