import tdl

from rogue import settings
from rogue.utils import colors


tdl.set_font(
    settings.GAME_FONT,
    greyscale=settings.GAME_FONT_GREYSCALE,
    altLayout=settings.GAME_FONT_ALTLAYOUT
)

root_console = tdl.init(
    settings.GAME_SCREEN_WIDTH,
    settings.GAME_SCREEN_HEIGHT,
    title=settings.GAME_TITLE,
    fullscreen=settings.GAME_FULLSCREEN
)

console = tdl.Console(
    settings.GAME_MAP_WIDTH,
    settings.GAME_MAP_HEIGHT
)

tdl.set_fps(settings.GAME_FPS)

panel = tdl.Console(
    settings.GAME_SCREEN_WIDTH,
    settings.IFACE_PANEL_HEIGHT
)


def print_str(x, y, msg, bg=None, fg=colors.white, fg_alpha=1.0, bg_alpha=0):
    """Prints a string

    This function will blit the string on the root console right away

    """
    _console = tdl.Console(len(msg), 1)
    _console.draw_str(
        0, 0, msg,
        bg=bg, fg=fg
    )
    root_console.blit(
        _console,
        x=x, y=y,
        width=len(msg), height=1,
        srcX=0, srcY=0,
        fg_alpha=fg_alpha, bg_alpha=bg_alpha
    )
    tdl.flush()
