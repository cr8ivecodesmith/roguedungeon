import os


BASEDIR = os.path.dirname(os.path.abspath(__file__))
PROJECTDIR = os.path.dirname(BASEDIR)
LOGDIR = os.path.join(PROJECTDIR, 'logs')
LOGFILE = os.path.join(PROJECTDIR, 'logs', 'game.log')

GAME_SCREEN_WIDTH = 80
GAME_SCREEN_HEIGHT = 50
GAME_TITLE = 'Rogue Dungeon'
GAME_FULLSCREEN = False
GAME_FPS = 20

GAME_FONT = os.path.join(BASEDIR, 'fonts', 'arial10x10.png')
GAME_FONT_GREYSCALE = True
GAME_FONT_ALTLAYOUT = True
