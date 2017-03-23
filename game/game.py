import logging

from .bootstrap import console, tdl

log = logging.getLogger('default')


def run():
    log.info('Game started')
    while not tdl.event.is_window_closed():
        console.draw_char(1, 1, '@', bg=None, fg=(255, 255, 255))
        tdl.flush()
