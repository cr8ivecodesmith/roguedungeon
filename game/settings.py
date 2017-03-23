import os


BASEDIR = os.path.dirname(os.path.abspath(__file__))
PROJECTDIR = os.path.dirname(BASEDIR)
LOGDIR = os.path.join(PROJECTDIR, 'logs')
LOGFILE = os.path.join(PROJECTDIR, 'logs', 'game.log')
DEBUG = True

GAME_SCREEN_WIDTH = 80
GAME_SCREEN_HEIGHT = 50
GAME_TITLE = 'Rogue Dungeon'
GAME_FULLSCREEN = False
GAME_FPS = 20
REALTIME_MOVEMENT = False

GAME_FONT = os.path.join(BASEDIR, 'fonts', 'arial10x10.png')
GAME_FONT_GREYSCALE = True
GAME_FONT_ALTLAYOUT = True

GAME_MAP_WIDTH = 80
GAME_MAP_HEIGHT = 45
COLOR_DARK_WALL = (0, 0, 100)
COLOR_DARK_GROUND = (50, 50, 150)
BG_CHAR_WALL = None
BG_CHAR_GROUND = None

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s %(name)s %(pathname)s %(lineno)d - %(message)s'
        },
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(module)s - %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGFILE,
            'maxBytes': 1024*1024*10,  # 10 megabytes
            'backupCount': 10,
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'default': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}
