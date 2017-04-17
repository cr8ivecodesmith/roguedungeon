import itertools as it
import logging
import textwrap

from rogue import settings
from rogue.consoles import panel, root_console, console, tdl
from rogue.generators.name import random_name
from rogue.handlers.status import GAME_STATUS, ENTITY_STATUS
from rogue.worlds.dungeon import Dungeon
from rogue.utils import colors


log = logging.getLogger('default')


class RenderManager:

    def __init__(self, world):
        self.world = world

    def all(self, mouse_coords=None):
        player = self.world.player
        if player.has_moved():
            player.compute_FOV()

        self.draw_dungeon_map()
        self.draw_entities()
        self.flush_console()
        self.draw_entities(clear=True)
        self.draw_panel(mouse_coords)
        self.draw_messages()
        self.flush_panel()

    def flush_console(self):
        # (Blit) the console to root_console
        root_console.blit(
            console,
            0, 0,
            settings.GAME_SCREEN_WIDTH, settings.GAME_SCREEN_HEIGHT,
            0, 0
        )
        tdl.flush()

    def flush_panel(self):
        root_console.blit(
            panel, 0,
            settings.IFACE_PANEL_Y, settings.GAME_SCREEN_WIDTH,
            settings.IFACE_PANEL_HEIGHT,
            0, 0
        )
        tdl.flush()

    def draw_dungeon_map(self):
        log.debug('Drawing dungeon map')

        player = self.world.player
        dungeon = self.world.player.dungeon

        for y in range(settings.GAME_MAP_HEIGHT):
            for x in range(settings.GAME_MAP_WIDTH):
                visible = (x, y) in player.visible_tiles
                wall = dungeon.dungeon_map[x][y].block_sight
                if not visible:
                    if dungeon.dungeon_map[x][y].explored:
                        if wall:
                            console.draw_char(
                                x, y, settings.WALL_CHAR,
                                fg=settings.WALL_FG_COLOR,
                                bg=settings.WALL_BG_COLOR_DARK
                            )
                        else:
                            console.draw_char(
                                x, y, settings.GROUND_CHAR,
                                fg=settings.GROUND_FG_COLOR,
                                bg=settings.GROUND_BG_COLOR_DARK
                            )
                else:
                    dungeon.dungeon_map[x][y].explored = True
                    if wall:
                        console.draw_char(
                            x, y, settings.WALL_CHAR,
                            fg=settings.WALL_FG_COLOR,
                            bg=settings.WALL_BG_COLOR_LIGHT
                        )
                    else:
                        console.draw_char(
                            x, y, settings.GROUND_CHAR,
                            fg=settings.GROUND_FG_COLOR,
                            bg=settings.GROUND_BG_COLOR_LIGHT
                        )

    def draw_entities(self, clear=False):
        log.debug('{} entities'.format('Clearing' if clear else 'Drawing'))
        dungeon = self.world.player.dungeon
        player = self.world.player

        # We split the monster list since we want to draw the dead ones first
        dead_monsters = [i for i in dungeon.entities.monsters
                         if i.status == ENTITY_STATUS.DEAD]
        monsters = [i for i in dungeon.entities.monsters
                    if i.status != ENTITY_STATUS.DEAD]

        for ent in it.chain(dead_monsters, dungeon.entities.loot, monsters):
            if clear:
                ent.clear()
            elif (ent.x, ent.y) in player.visible_tiles:
                ent.draw()

        if clear:
            player.clear()
        else:
            player.draw()

    def draw_panel(self, mouse_coords=None):
        player = self.world.player

        panel.clear(fg=colors.white, bg=colors.black)
        self.draw_bar(
            1, 1,
            settings.IFACE_BAR_WIDTH, 'HP',
            player.fighter.hp, player.fighter.max_hp,
            colors.light_red, colors.dark_red
        )

        names_under_mouse = self.get_names_under_mouse(mouse_coords)
        if names_under_mouse:
            panel.draw_str(
                1, 0, names_under_mouse,
                bg=None, fg=colors.light_gray
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
        for line, color in self.world.messages:
            panel.draw_str(settings.MSG_X, y, line, bg=None, fg=color)
            y += 1

    def get_names_under_mouse(self, coords=None):
        if not coords:
            return
        x, y = coords
        dungeon = self.world.player.dungeon
        visible = self.world.player.visible_tiles
        names = [e.name for e in dungeon.entities.all(iterator=True)
                 if (e.x, e.y) == coords and (e.x, e.y) in visible]
        return (', '.join(names)).capitalize()


class GameWorld:
    def __init__(self):
        self.status = GAME_STATUS.PLAY
        self.messages = []
        self.dungeons = []
        self.player = None

        self.render = RenderManager(world=self)

    def generate_dungeon(self):
        depth = 0 if not self.dungeons else len(self.dungeons)
        name = (random_name()).title()
        dungeon = Dungeon(world=self, name=name, depth=depth)
        self.dungeons.append(dungeon)
        return dungeon

    def message(self, msg, color=colors.white):
        msg_lines = textwrap.wrap(msg, settings.MSG_WIDTH)
        for line in msg_lines:
            if len(self.messages) >= settings.MSG_HEIGHT:
                del self.messages[0]
            self.messages.append((line, color))
