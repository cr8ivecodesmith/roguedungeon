import textwrap

from rogue import settings
from rogue.consoles import panel, root_console
from rogue.generators.name import random_name
from rogue.handlers.status import GAME_STATUS
from rogue.worlds.dungeon import Dungeon
from rogue.utils import colors


class RenderManager:
    def __init__(self, gameworld):
        self.gameworld = gameworld

    def flush(self):
        root_console.blit(
            panel, 0,
            settings.IFACE_PANEL_Y, settings.GAME_SCREEN_WIDTH,
            settings.IFACE_PANEL_HEIGHT,
            0, 0
        )

    def draw_bar(
        self, x, y, total_width,
        name, value, maximum,
        bar_color, back_color
    ):
        bar_width = int(float(value) / maximum * total_width)
        panel.draw_rect(x, y, total_width, 1, None, bg=back_color)
        if bar_width > 0:
            panel.draw_rect(x, y, bar_width, 1, None, bg=bar_color)
        text = '{}: {}/{}'.format(name, value, maximum)
        x_centered = x + (total_width - len(text)) // 2
        panel.draw_str(x_centered, y, text, fg=colors.white, bg=None)

    def draw_messages(self):
        y = 1
        for line, color in self.gameworld.messages:
            panel.draw_str(settings.MSG_X, y, line, bg=None, fg=color)
            y += 1


class GameWorld:
    def __init__(self):
        self.status = GAME_STATUS.PLAY
        self.messages = []
        self.dungeons = []
        self.current_dungeon = None
        self.render = RenderManager(self)

    def generate_dungeon(self, current=False):
        depth = 0 if not self.dungeons else len(self.dungeons)
        name = (random_name()).title()
        dungeon = Dungeon(world=self, name=name, depth=depth)
        self.dungeons.append(dungeon)
        if current:
            self.current_dungeon = dungeon
        return dungeon

    def message(self, msg, color=colors.white):
        msg_lines = textwrap.wrap(msg, settings.MSG_WIDTH)
        for line in msg_lines:
            if len(self.messages) >= settings.MSG_HEIGHT:
                del self.messages[0]
            self.messages.append((line, color))
