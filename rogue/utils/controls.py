import logging

from rogue import settings
from rogue.consoles import tdl


log = logging.getLogger('default')


def get_user_input():
    """Returns the user input object
    Returns none when there's no activity during realtime movement

    """
    user_input = None
    if not settings.REALTIME_MOVEMENT:
        user_input = tdl.event.key_wait()
    else:
        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
    return user_input


def get_move_direction(user_input):
    """Determine the direction of movement

    """
    direction = None
    if (user_input.key == 'UP' or 
        (user_input.key == 'CHAR' and user_input.char == 'k')):
        direction = 'up'
    elif (user_input.key == 'DOWN' or 
        (user_input.key == 'CHAR' and user_input.char == 'j')):
        direction = 'down'
        has_moved = True
    elif (user_input.key == 'LEFT' or 
        (user_input.key == 'CHAR' and user_input.char == 'h')):
        direction = 'left'
    elif (user_input.key == 'RIGHT' or 
        (user_input.key == 'CHAR' and user_input.char == 'l')):
        direction = 'right'
    elif user_input.key == 'CHAR' and user_input.char == 'y':
        direction = 'up+left'
    elif user_input.key == 'CHAR' and user_input.char == 'u':
        direction = 'up+right'
    elif user_input.key == 'CHAR' and user_input.char == 'b':
        direction = 'down+left'
    elif user_input.key == 'CHAR' and user_input.char == 'n':
        direction = 'down+right'
    return direction


def get_move_amount(direction):
    """Determine amount of movement based on direction

    """
    amount = {
        'up': (0, -1),
        'down': (0, 1),
        'left': (-1, 0),
        'right': (1, 0),
        'up+left': (-1, -1),
        'up+right': (1, -1),
        'down+left': (-1, 1),
        'down+right': (1, 1),
    }
    return amount.get(direction, (0, 0))
