from .bootstrap import console, tdl


def run():
    while not tdl.event.is_window_closed():
        console.draw_char(1, 1, '@', bg=None, fg=(255, 255, 255))
        tdl.flush()
