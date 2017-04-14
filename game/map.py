import logging

from random import randint

from . import settings as st


log = logging.getLogger('default')


def create_room(gamemap, room):
    """Carves a room in the gamemap

    """
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            gamemap[x][y].blocked = False
            gamemap[x][y].block_sight = False
    return gamemap


def create_h_tunnel(gamemap, y, x1, x2):
    """Creates a horizontal tunnel

    """
    for x in range(min(x1, x2), max(x1, x2) + 1):
        gamemap[x][y].blocked = False
        gamemap[x][y].block_sight = False
    return gamemap


def create_v_tunnel(gamemap, x, y1, y2):
    """Creates a vertical tunnel

    """
    for y in range(min(y1, y2), max(y1, y2) + 1):
        gamemap[x][y].blocked = False
        gamemap[x][y].block_sight = False
    return gamemap


def is_visible_tile(gamemap, x, y):
    """Determines tile visibility. Used primarily for FOV determination

    """
    if x >= st.GAME_MAP_WIDTH or x < 0:
        return False
    elif y >= st.GAME_MAP_HEIGHT or y < 0:
        return False
    elif gamemap[x][y].blocked:
        return False
    elif gamemap[x][y].block_sight:
        return False
    else:
        return True


def generate_gamemap():
    """Generate the gamemap

    """
    from .entities import Tile, Rect

    log.debug('Generating gamemap')

    # Fill map with `blocked` tile
    gamemap = [[ Tile(True) for y in range(st.GAME_MAP_HEIGHT)]
                for x in range(st.GAME_MAP_WIDTH) ]

    rooms = []
    num_rooms = 0
    for r in range(st.MAX_ROOMS):
        # Get random width and height
        w = randint(st.ROOM_MIN_SIZE, st.ROOM_MAX_SIZE)
        h = randint(st.ROOM_MIN_SIZE, st.ROOM_MAX_SIZE)

        # Get random pos w/o going out of the map bounds
        x = randint(0, st.GAME_MAP_WIDTH - w - 1)
        y = randint(0, st.GAME_MAP_HEIGHT - h - 1)

        new_room = Rect(x, y, w, h)

        # Run through the other rooms to see if they intersect
        failed = False
        for other_room in rooms:
            if new_room.intersect(other_room):
                failed = True
                break

        if not failed:
            gamemap = create_room(gamemap, new_room)
            new_x, new_y = new_room.center()
            if num_rooms >= 1:
                prev_x, prev_y = rooms[num_rooms - 1].center()
                # Randomly pick a how to carve the tunnels
                if randint(0, 1):
                    # Move horizontally, then vertically
                    gamemap = create_h_tunnel(gamemap, prev_y, prev_x, new_x)
                    gamemap = create_v_tunnel(gamemap, new_x, prev_y, new_y)
                else:
                    # Move vertically, then horizontally
                    gamemap = create_v_tunnel(gamemap, prev_x, prev_y, new_y)
                    gamemap = create_h_tunnel(gamemap, new_y, prev_x, new_x)
            rooms.append(new_room)
            num_rooms += 1
            log.debug('Room created at {} [{}]'.format(
                new_room.center(), len(rooms)
            ))

    return gamemap, rooms


gamemap, rooms = generate_gamemap()
