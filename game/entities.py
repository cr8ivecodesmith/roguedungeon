from .bootstrap import console


class GameObject:
    """A generic object that represents anything on the screen (i.e. player,
    monster, item, stairs, wall, etc.

    """
    def __init__(self, x, y, char, name, color, blocks=False):
        self.x, self.y = x, y
        self.char, self.name, self.color = char, name, color
        self.blocks = blocks

    def move(self, dx, dy):
        """Move by the given amount

        """
        from .map import gamemap, rooms, is_blocked

        if not is_blocked(gamemap, rooms, self.x, self.y):
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
        self.explored = False
        self.blocked = blocked

        # If a tile is blocked, it also blocks sight
        self.block_sight = blocked if blocked else block_sight


class Rect:
    """A rectangle on the map used to characterize a room

    """
    def __init__(self, x, y, w, h):
        self.x1, self.y1 = x, y
        self.x2, self.y2 = (x + w), (y + h)
        self.room_objects = []

    def center(self):
        """Returns the center coordinate of the room
        Primarily used to connect the room with tunnels

        """
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return center_x, center_y

    def intersect(self, other):
        """Returns true when this room intersects with `other` room

        """
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)
