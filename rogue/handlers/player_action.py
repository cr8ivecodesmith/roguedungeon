import logging
import sys

from rogue.utils.controls import get_move_direction, get_move_amount


log = logging.getLogger('default')


def process(dungeon, user_input=None):
    if not user_input:
        return
    player = dungeon.entities.player

    move_direction = get_move_direction(user_input)
    move_amount = get_move_amount(move_direction)
    player.move(*move_amount)

    log.debug('Player has moved [{}] from {} to {}'.format(
        player.has_moved(),
        (player.prev_x, player.prev_y),
        (player.x, player.y)
    ))
