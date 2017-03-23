from logging import config as log_conf
import os

import tdl

from . import settings as st

tdl.set_font(
    st.GAME_FONT,
    greyscale=st.GAME_FONT_GREYSCALE,
    altLayout=st.GAME_FONT_ALTLAYOUT
)

root_console = tdl.init(
    st.GAME_SCREEN_WIDTH,
    st.GAME_SCREEN_HEIGHT,
    title=st.GAME_TITLE,
    fullscreen=st.GAME_FULLSCREEN
)

console = tdl.Console(
    st.GAME_SCREEN_WIDTH,
    st.GAME_SCREEN_HEIGHT
)

tdl.setFPS(st.GAME_FPS)


def setup_logging():
    if not os.path.isdir(st.LOGDIR):
        os.mkdir(st.LOGDIR)
    if not os.path.exists(st.LOGFILE):
        with open(st.LOGFILE, 'w') as fh:
            fh.close()
    log_conf.dictConfig(st.LOGGING)


def init():
    setup_logging()
