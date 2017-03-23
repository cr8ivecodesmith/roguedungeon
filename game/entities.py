from .bootstrap import console


class GameObject:
    """A generic object that represents anything on the screen (i.e. player,
    monster, item, stairs, wall, etc.

    """
    def __init__(self, x, y, char, color):
        self.x, self.y = x, y
        self.char, self.color = char, color

    def move(self, dx, dy):
        """Move by the given amount

        """
        from .map import gamemap

        movable = (
            not gamemap[self.x + dx][self.y + dy].blocked
            and dx != None != dy
        )

        if movable:
            self.x += dx
            self.y += dy

    def draw(self):
        """Draw the character at this position

        """
        console.draw_char(self.x, self.y, self.char, self.color)

    def clear(self):
        """Clear the character at this position

        """
        console.draw_char(self.x, self.y, ' ', self.color, bg=None)


class Tile:
    """A tile entity and its properties

    """
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        # If a tile is blocked, it also blocks sight
        self.block_sight = blocked if blocked else block_sight
