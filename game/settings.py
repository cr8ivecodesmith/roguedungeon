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

WALL_CHAR = None
WALL_FG_COLOR = None
WALL_BG_COLOR_DARK = (0, 0, 100)

GROUND_CHAR = None
GROUND_FG_COLOR = None
GROUND_BG_COLOR_DARK = (50, 50, 150)

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
