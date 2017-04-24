import itertools as it
from string import whitespace
from textwrap import wrap

import tdl

from rogue import settings
from rogue.utils import colors
from rogue.utils.controls import get_char_or_cancel


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

overlay = tdl.Console(
    settings.GAME_SCREEN_WIDTH,
    settings.GAME_SCREEN_HEIGHT
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


def message_box(
    x, y, msg, width=50,
    fg=colors.white,
    fg_alpha=1.0, bg_alpha=0.75
):
    """Prints a message prompt that waits for user input to dismiss

    """
    _console = tdl.Console(
        settings.GAME_SCREEN_WIDTH, settings.GAME_SCREEN_HEIGHT,
    )
    _console.set_colors(fg=fg)
    _console.set_mode('scroll')
    _console.print_str(msg)

    root_console.blit(
        overlay,
        0, 0,
        settings.GAME_SCREEN_WIDTH, settings.GAME_SCREEN_HEIGHT,
        0, 0,
        fg_alpha=fg_alpha, bg_alpha=bg_alpha
    )
    root_console.blit(
        _console,
        x, y,
        width, None,
        0, 0,
        fg_alpha=fg_alpha, bg_alpha=0
    )
    tdl.flush()

    # Wait for user to enter any letter key or the ESC key before
    # dismissing
    get_char_or_cancel()
