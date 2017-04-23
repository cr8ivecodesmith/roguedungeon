import os


# Path settings
BASEDIR = os.path.dirname(os.path.abspath(__file__))
PROJECTDIR = os.path.dirname(BASEDIR)
DATADIR = os.path.join(BASEDIR, 'data')
LOGDIR = os.path.join(PROJECTDIR, 'logs')


# Game settings
GAME_SCREEN_WIDTH = 80
GAME_SCREEN_HEIGHT = 50
GAME_TITLE = 'Rogue Dungeon'
GAME_FULLSCREEN = False
GAME_FPS = 20
REALTIME = True

GAME_FONT = os.path.join(BASEDIR, 'fonts', 'terminal10x10.png')
GAME_FONT_GREYSCALE = True
GAME_FONT_ALTLAYOUT = True

GAME_MAP_WIDTH = 80
GAME_MAP_HEIGHT = 43

IFACE_BAR_WIDTH = 20
IFACE_PANEL_HEIGHT = 7
IFACE_PANEL_Y = GAME_SCREEN_HEIGHT - IFACE_PANEL_HEIGHT
INVENTORY_WIDTH = 50
LEVEL_SCREEN_WIDTH = 40

MSG_X = IFACE_BAR_WIDTH + 2
MSG_WIDTH = GAME_SCREEN_WIDTH - IFACE_BAR_WIDTH - 2
MSG_HEIGHT = IFACE_PANEL_HEIGHT - 1

MAX_ROOMS = 30
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
ROOM_MAX_MONSTERS = 3
ROOM_MAX_ITEMS = 2

PLAYER_MAX_INVENTORY = 26
PLAYER_LEVEL_UP_BASE = 200
PLAYER_LEVEL_UP_FACTOR = 150

SPELL_HEAL_AMOUNT = 10
SPELL_LIGHTNING_RANGE = 20
SPELL_LIGHTNING_DAMAGE = 10
SPELL_CONFUSE_NUM_TURNS = 10
SPELL_CONFUSE_RANGE = 10
SPELL_FIREBALL_RADIUS = 3
SPELL_FIREBALL_DAMAGE = 25

WALL_CHAR = None
WALL_FG_COLOR = None
WALL_BG_COLOR_DARK = (0, 0, 100)
WALL_BG_COLOR_LIGHT = (130, 110, 50)

GROUND_CHAR = None
GROUND_FG_COLOR = None
GROUND_BG_COLOR_DARK = (50, 50, 150)
GROUND_BG_COLOR_LIGHT = (200, 180, 50)

FOV_ALGO = 'BASIC'
FOV_LIGHT_WALLS = True
FOV_TORCH_RADIUS = 10


# Log settings
DEBUG = True
LOGLEVEL = 'INFO'
LOGFILE = os.path.join(PROJECTDIR, 'logs', 'game.log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('[%(asctime)s] %(levelname)s %(name)s %(pathname)s '
                       '%(lineno)d - %(message)s')
        },
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(module)s - %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG' if DEBUG else LOGLEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGFILE,
            'maxBytes': 1024 * 1024 * 10,  # 10 megabytes
            'backupCount': 10,
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG' if DEBUG else LOGLEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'default': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG' if DEBUG else LOGLEVEL,
            'propagate': False,
        },
    },
}
