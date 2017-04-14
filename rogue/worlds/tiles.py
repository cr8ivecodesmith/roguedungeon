class Tile:
    """A tile entity and its properties

    """
    def __init__(self, blocked, block_sight=None, explored=False):
        self.explored = explored
        self.blocked = blocked

        # If a tile is blocked, it also blocks sight
        self.block_sight = blocked if blocked else block_sight
