import logging

from random import randint

from rogue import settings
from rogue.worlds.tiles import Tile
from rogue.worlds.rooms import Room


log = logging.getLogger('default')


class MapManager:
    def __init__(self, dungeon):
        self.dungeon = dungeon

        # Attach the `dungeon_map` attribute
        self.dungeon.dungeon_map = self.init_dungeon_map()

    def init_dungeon_map(self):
        log.debug('Initializing {}x{} dungeon map'.format(
            settings.GAME_MAP_WIDTH,
            settings.GAME_MAP_HEIGHT
        ))
        dungeon_map = [[Tile(True) for y in range(settings.GAME_MAP_HEIGHT)]
                       for x in range(settings.GAME_MAP_WIDTH)]
        return dungeon_map

    def is_visible_tile(self, x, y):
        """Determines tile visibility. Used primarily for FOV determination

        """
        if x >= settings.GAME_MAP_WIDTH or x < 0:
            return False
        elif y >= settings.GAME_MAP_HEIGHT or y < 0:
            return False
        elif self.dungeon.dungeon_map[x][y].blocked:
            return False
        elif self.dungeon.dungeon_map[x][y].block_sight:
            return False
        else:
            return True

    def is_blocked(self, x, y):
        """Determines if a tile is blocked by a blocking object

        """
        if self.dungeon.dungeon_map[x][y].blocked:
            return True
        if hasattr(self.dungeon, 'entities'):
            for ent in self.dungeon.entities.all(iterator=True):
                if ent.blocks and ent.x == x and ent.y == y:
                    return True
        return False


class RoomManager:
    """Manages dungeon rooms

    Requires:
    - MapManager

    """
    def __init__(self, dungeon):
        self.dungeon = dungeon

        # Attach the `rooms` attribute
        self.dungeon.rooms = self.init_dungeon_rooms()

    def init_dungeon_rooms(self):
        log.debug('Initializing dugeon rooms')
        rooms = []
        num_rooms = 0

        for r in range(settings.MAX_ROOMS):
            # Get random width and height
            w = randint(settings.ROOM_MIN_SIZE, settings.ROOM_MAX_SIZE)
            h = randint(settings.ROOM_MIN_SIZE, settings.ROOM_MAX_SIZE)

            # Get random pos w/o going out of the map bounds
            x = randint(0, settings.GAME_MAP_WIDTH - w - 1)
            y = randint(0, settings.GAME_MAP_HEIGHT - h - 1)

            new_room = Room(x, y, w, h)

            # Run through the other rooms to see if they intersect
            failed = False
            for other_room in rooms:
                if new_room.intersect(other_room):
                    failed = True
                    break

            if not failed:
                self.carve_room(new_room)
                new_x, new_y = new_room.center()
                if num_rooms >= 1:
                    prev_x, prev_y = rooms[num_rooms - 1].center()
                    # Randomly pick a how to carve the tunnels
                    if randint(0, 1):
                        # Move horizontally, then vertically
                        self.carve_h_tunnel(prev_y, prev_x, new_x)
                        self.carve_v_tunnel(new_x, prev_y, new_y)
                    else:
                        # Move vertically, then horizontally
                        self.carve_v_tunnel(prev_x, prev_y, new_y)
                        self.carve_h_tunnel(new_y, prev_x, new_x)
                rooms.append(new_room)

                num_rooms += 1
                log.debug('Room created at {} [{}]'.format(
                    new_room.center(), len(rooms)
                ))

        return rooms

    def carve_room(self, room):
        """Carves a room on the dungeon map based on the room dimensions

        """
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.dungeon.dungeon_map[x][y].blocked = False
                self.dungeon.dungeon_map[x][y].block_sight = False

    def carve_h_tunnel(self, y, x1, x2):
        """Carves a horizontal tunnel on the dungeon map based on the given
        dimensions

        """
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.dungeon.dungeon_map[x][y].blocked = False
            self.dungeon.dungeon_map[x][y].block_sight = False

    def carve_v_tunnel(self, x, y1, y2):
        """Carves a vertical tunnel on the dungeon map based on the given
        dimensions

        """
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.dungeon.dungeon_map[x][y].blocked = False
            self.dungeon.dungeon_map[x][y].block_sight = False


class EntityManager:
    """Manages dungeon entities

    Requires:
    - MapManager
    - RoomManager

    """
    def __init__(self, dungeon):
        self.dungeon = dungeon
        self._entities = {
            'monster': [],
            'loot': [],
            'npc': [],
        }

    @property
    def monsters(self):
        return self._entities.get('monster')

    @property
    def loot(self):
        return self._entities.get('loot')

    @property
    def npcs(self):
        return self._entities.get('npc')

    def all(self, iterator=False):
        ents = []
        for group in self._entities.values():
            if not iterator:
                ents.extend(group)
                continue
            else:
                for ent in group:
                    yield ent
        return ents

    def add(self, kind, entity):
        entity.dungeon = self.dungeon
        self._entities[kind].append(entity)


class Dungeon:

    def __init__(self, world, name, depth):
        self.world = world
        self.name = name
        self.depth = depth

        # Initializes the `dungeon_map` attribute
        self.map_manager = MapManager(self)

        # Initializes the `rooms` attribute
        self.room_manager = RoomManager(self)

        # Creates the `entities` attribute
        self.entities = EntityManager(self)

    def __str__(self):
        return '{} ({})'.format(self.name, self.depth)
