import logging
import sys


log = logging.getLogger('default')


def process(user_input=None):
    if not user_input:
        return

    if user_input.key == 'ESCAPE':
        log.debug('Smell ya later!')
        sys.exit()
