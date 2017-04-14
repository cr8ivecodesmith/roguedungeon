import logging
import sys


log = logging.getLogger('default')

DO_QUIT = 'quit'
DO_PLAY = 'play'


def process(user_input):
    if not user_input:
        return
    if user_input.key == 'ESCAPE':
        return DO_QUIT
    else:
        return DO_PLAY
