import logging

from rogue.handlers.game import new_game, play_game, main_menu


log = logging.getLogger('default')


def run():
    main_menu()
