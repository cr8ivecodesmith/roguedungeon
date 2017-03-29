from . import settings as st


def __generate_gamemap():
    from .entities import Tile
    gamemap = [[ Tile(False) for y in range(st.GAME_MAP_HEIGHT)]
                for x in range(st.GAME_MAP_WIDTH) ]

    # Make some impromptu pillars
    gamemap[30][22].blocked = True
    gamemap[30][22].block_sight = True
    gamemap[50][22].blocked = True
    gamemap[50][22].block_sight = True

    return gamemap


gamemap = __generate_gamemap()
