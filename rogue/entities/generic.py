import logging

from rogue.consoles import console


log = logging.getLogger('default')


class GameObject:
    """A generic object that represents anything on the dungeon (i.e. player,
    monster, item, stairs, wall, etc.

    """
    def __init__(self,
        x, y,
        char, name, color,
        blocks=False,
        speed=1,
        dungeon=None
    ):
        self._x, self._y = x, y
        self.prev_x, self.prev_y = x, y

        self.char, self.name, self.color = char, name, color
        self.blocks = blocks
        self.speed = speed
        self.dungeon = dungeon

    def __str__(self):
        return '{}@{}'.format(
            self.name,
            (self.x, self.y)
        )

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        self.prev_x = self._x
        self._x = val

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, val):
        self.prev_y = self._y
        self._y = val

    def has_moved(self):
        return (self.prev_x, self.prev_y) != (self.x, self.y)

    def move(self, dx, dy):
        """Move by the given amount

        """
        new_x, new_y = (dx * self.speed), (dy * self.speed)
        passable = (
            self.dungeon and
            not self.dungeon.map_manager.is_blocked(
                self.x + new_x, self.y + new_y
            )
        )
        if passable:
            self.x += new_x
            self.y += new_y

    def draw(self):
        """Draw the character at this position

        """
        console.draw_char(self.x, self.y, self.char, self.color)

    def clear(self):
        """Clear the character at this position

        """
        console.draw_char(self.x, self.y, ' ', self.color, bg=None)
