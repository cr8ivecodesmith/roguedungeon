import tdl

from rogue import settings


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
    settings.GAME_SCREEN_WIDTH,
    settings.GAME_SCREEN_HEIGHT
)

tdl.setFPS(settings.GAME_FPS)
