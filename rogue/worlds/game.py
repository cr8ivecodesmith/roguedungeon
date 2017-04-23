import itertools as it
import logging
import textwrap

from rogue import settings
from rogue.consoles import panel, root_console, console, tdl
from rogue.handlers.status import GAME_STATUS, ENTITY_STATUS
from rogue.worlds.dungeon import Dungeon
from rogue.utils import colors
from rogue.utils.name_generator import random_name
from rogue.utils.controls import get_char_or_cancel


log = logging.getLogger('default')


class RenderManager:

    def __init__(self, world):
        self.world = world

    def all(self, mouse_coords=None):
        player = self.world.player
        if player.has_moved():
            player.compute_FOV()

        player.check_level_up()

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
        dungeon = self.world.player.dungeon
        dungeon_map = dungeon.dungeon_map
        player = self.world.player

        # We split the monster list since we want to draw the dead ones first
        dead_monsters = (i for i in dungeon.entities.monsters
                         if i.status == ENTITY_STATUS.DEAD)
        live_monsters = (i for i in dungeon.entities.monsters
                         if i.status != ENTITY_STATUS.DEAD)
        entities = it.chain(
            dead_monsters,
            dungeon.stairs.values(),
            dungeon.entities.loot,
            live_monsters
        )

        for ent in entities:
            mx, my = ent.coords()
            show = (
                (ent.always_visible and dungeon_map[mx][my].explored) or
                ent.coords() in player.visible_tiles
            )
            if clear:
                ent.clear()
            elif show:
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
        panel.draw_str(
            1, 2,
            'Dungeon level {}'.format(player.dungeon.depth + 1),
            bg=None, fg=colors.white
        )
        panel.draw_str(
            1, 3,
            'Player level {}'.format(player.level),
            bg=None, fg=colors.white
        )
        panel.draw_str(
            1, 4,
            'XP {}/{}'.format(player.fighter.xp, player.next_level_xp),
            bg=None, fg=colors.white
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
        player = self.world.player
        dungeon = player.dungeon
        visible = player.visible_tiles
        names = [e.name for e in dungeon.entities.all(iterator=True)
                 if e.coords() == coords and e.coords() in visible]
        names.extend(e.name for e in dungeon.stairs.values()
                     if e.coords() == coords and e.coords() in visible)
        if player.coords() == coords:
            names.append(player.name)
        return (', '.join(names)).capitalize()

    def menu(self, header, options, width):
        max_menu_options = 26
        if len(options) > max_menu_options:
            err = 'Cannot have a menu with more than {} options!'.format(
                max_menu_options
            )
            raise ValueError(err)

        # Calc the wrapped header height and one line per option
        header_wrapped = textwrap.wrap(header, width)
        header_height = len(header_wrapped)
        height = len(options) + header_height

        # Create an off-screen window that reps the menu's window
        window = tdl.Console(width, height)

        # Print the header with wrapped text
        window.draw_rect(
            0, 0,
            width, height,
            None, fg=colors.white, bg=None
        )
        for i, line in enumerate(header_wrapped):
            window.draw_str(0, 0 + i, header_wrapped[i])

        # Print the menu options
        y = header_height
        letter_idx = ord('a')
        for opt_text in options:
            text = '({}) {}'.format(
                chr(letter_idx), opt_text
            )
            window.draw_str(0, y, text, bg=None)
            y += 1
            letter_idx += 1

        # Blit the window console to root_console
        x = settings.GAME_SCREEN_WIDTH // 2 - width // 2
        y = settings.GAME_SCREEN_HEIGHT // 2 - height // 2
        root_console.blit(window, x, y, width, height, 0, 0)

        # Present the console to the player and wait for keypress
        tdl.flush()
        log.debug('Waiting for user input...')
        key = get_char_or_cancel()
        log.debug(key)
        key_char = key.char
        if key_char == '':
            key_char = ' '  # placeholder

        # Return the option index the keypress correlates to
        idx = ord(key_char) - ord('a')
        if idx >= 0 and idx < len(options):
            return idx

        return None

    def inventory_menu(self, drop=False, header=None):
        header = header or (
            'Press the key next to an item to {} it, '
            'or [ESC] to cancel.\n'.format(
                'drop' if drop else 'use'
            )
        )
        inventory = self.world.player.inventory
        opts = []
        if not inventory:
            opts.append('Inventory is empty.')
        else:
            for i in inventory:
                text = i.name
                if i.equipment and i.equipment.is_equipped:
                    text = '{} (on {})'.format(i.name, i.equipment.slot)
                opts.append(text)

        idx = self.menu(header, opts, settings.INVENTORY_WIDTH)

        if idx is None or not inventory:
            return None

        return inventory[idx].item


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

    def message(self, msg, color=colors.white, force_render=False):
        msg_lines = textwrap.wrap(msg, settings.MSG_WIDTH)
        for line in msg_lines:
            if len(self.messages) >= settings.MSG_HEIGHT:
                del self.messages[0]
            self.messages.append((line, color))
        if force_render:
            self.render.all()

    def message_box(self, msg, width=50, force_render=False):
        self.render.menu(msg, [], width)
        if force_render:
            self.render.all()
