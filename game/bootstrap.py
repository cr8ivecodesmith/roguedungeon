import os
import tdl
from . import settings as st

tdl.set_font(
    st.GAME_FONT,
    greyscale=st.GAME_FONT_GREYSCALE,
    altLayout=st.GAME_FONT_ALTLAYOUT
)

console = tdl.init(
    st.GAME_SCREEN_WIDTH,
    st.GAME_SCREEN_HEIGHT,
    title=st.GAME_TITLE,
    fullscreen=st.GAME_FULLSCREEN
)

tdl.setFPS(st.GAME_FPS)


def create_logging():
    if not os.path.isdir(st.LOGDIR):
        os.mkdir(st.LOGDIR)
    if not os.path.exists(st.LOGFILE):
        with open(st.LOGFILE, 'w') as fh:
            fh.close()


def init():
    create_logging()
