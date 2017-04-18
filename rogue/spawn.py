import logging
from random import randint

from rogue import settings
from rogue.entities.components.fighters import FighterComponent
from rogue.entities.components.monsters import BasicMonsterAIComponent
from rogue.entities.components.loot import ItemComponent
from rogue.entities.generic import GameObject
from rogue.entities.player import Player
from rogue.handlers.death import monster_death
from rogue.handlers.spells import cast_heal
from rogue.utils import colors


log = logging.getLogger('default')


def spawn_player(gameworld, dungeon):
    """Initializes the player on the first room

    """
    player = Player(world=gameworld)
    gameworld.player = player
    player.dungeon = dungeon
    player.x, player.y = dungeon.rooms[0].center()
    log.debug('{} placed at {}'.format(player.name, (player.x, player.y)))


def spawn_monsters(dungeon):
    """Spawn dungeon monsters

    """
    for idx, room in enumerate(dungeon.rooms):
        num_monsters = randint(0, settings.ROOM_MAX_MONSTERS)
        log.debug('Generating {} monsters in room {}'.format(
            num_monsters, idx+1
        ))
        for i in range(num_monsters):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
            chance = randint(0, 100)
            fighter_opts = {
                'death_handler': monster_death,
            }
            obj_opts = {
                'x': x,
                'y': y,
                'blocks': True,
                'dungeon': dungeon,
            }
            if chance < 80:
                # create an orc
                fighter_opts['hp'] = 10
                fighter_opts['defense'] = 0
                fighter_opts['power'] = 3
                obj_opts['char'] = 'o'
                obj_opts['name'] = 'Orc'
                obj_opts['color'] = colors.desaturated_green
            else:
                # create a troll
                fighter_opts['hp'] = 16
                fighter_opts['defense'] = 1
                fighter_opts['power'] = 4
                obj_opts['char'] = 'T'
                obj_opts['name'] = 'Troll'
                obj_opts['color'] = colors.darker_green

            ai_component = BasicMonsterAIComponent()
            fighter_component = FighterComponent(**fighter_opts)
            obj_opts['ai'] = ai_component
            obj_opts['fighter'] = fighter_component
            obj = GameObject(**obj_opts)
            dungeon.entities.monsters.append(obj)


def spawn_loot(dungeon):
    """Spawn Items

    """
    for idx, room in enumerate(dungeon.rooms):
        num_items = randint(0, settings.ROOM_MAX_ITEMS)
        log.debug('Generating {} items in room {}'.format(
            num_items, idx+1
        ))
        for i in range(num_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if dungeon.map_manager.is_blocked(x, y):
                # Only place the item on non-blocked tile
                continue

            # chance = randint(0, 100)
            obj_opts = {
                'x': x,
                'y': y,
                'dungeon': dungeon,
            }

            obj_opts['char'] = '!'
            obj_opts['name'] = 'Healing Potion'
            obj_opts['color'] = colors.violet
            obj_opts['item'] = ItemComponent(use_handler=cast_heal)

            obj = GameObject(**obj_opts)
            dungeon.entities.loot.append(obj)
