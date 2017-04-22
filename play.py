#!/usr/bin/env python
from rogue import bootstrap
from rogue.handlers.game import main_menu


if __name__ == '__main__':
    bootstrap.init()
    main_menu()
