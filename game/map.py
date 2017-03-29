from . import settings as st


def create_room(room, gamemap):
    """Carves a room in the gamemap

    """
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            gamemap[x][y].blocked = False
            gamemap[x][y].block_sight = False
    return gamemap


def __generate_gamemap():
    from .entities import Tile, Rect

    # Fill map with `blocked` tile
    gamemap = [[ Tile(True) for y in range(st.GAME_MAP_HEIGHT)]
                for x in range(st.GAME_MAP_WIDTH) ]

    # Create 2 rooms
    room1 = Rect(20, 15, 10, 15)
    room2 = Rect(50, 15, 10, 15)

    gamemap = create_room(room1, gamemap)
    gamemap = create_room(room2, gamemap)

    return gamemap


gamemap = __generate_gamemap()
