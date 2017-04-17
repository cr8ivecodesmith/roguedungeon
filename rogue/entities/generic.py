import logging
import math

from rogue import settings
from rogue.consoles import tdl, console
from rogue.handlers.status import ENTITY_STATUS


log = logging.getLogger('default')


class GameObject:
    """A generic object that represents anything on the dungeon (i.e. player,
    monster, item, stairs, wall, etc.

    """
    __dungeon = None
    __visible_tiles = []

    def __init__(
        self, x, y,
        char, name, color,
        blocks=False, always_visible=False,
        fighter=None, ai=None, item=None, equipment=None,
        speed=1, dungeon=None
    ):
        self._x, self._y = x, y
        self.prev_x, self.prev_y = x, y

        self.char, self.name, self.color = char, name, color
        self.blocks = blocks
        self.always_visible = always_visible
        self.speed = speed
        self.dungeon = dungeon
        self.status = ENTITY_STATUS.NO_ACTION

        # Set components
        self.fighter = fighter
        if fighter:
            self.fighter.owner = self

        self.ai = ai
        if ai:
            self.ai.owner = self

        self.item = item
        if item:
            self.item.owner = self

        self.equipment = equipment
        if equipment:
            self.equipment.owner = self

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

    @property
    def dungeon(self):
        return self.__dungeon

    @dungeon.setter
    def dungeon(self, val):
        self.__dungeon = val
        if self.__dungeon and self.fighter:
            # Compute FOV when a new dungeon is assigned for fighter types
            self.compute_FOV()

    @property
    def visible_tiles(self):
        return self.__visible_tiles

    @visible_tiles.setter
    def visible_tiles(self, val):
        self.__visible_tiles = val

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

    def move_towards(self, target_x, target_y):
        """Basic path-finding functionality.

        Get a vector from the object to the target, then normalize so it has
        the same direction but has a length of exactly 1 tile. Then we round it
        so the resulting vector is an integer and not a fraction (dx and dy can
        only take values that is -1, 1, or 0). Finally, the object moves by
        this amount.

        """
        # vector and distance from this object to its target
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        # normalize it to lenght 1 (preserving direction), then round it and
        # convert to int so the movement is restricted to the map grid.
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.move(dx, dy)

    def distance_to(self, other):
        """Return the distance to another object.

        """
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx**2 + dy**2)

    def distance(self, x, y):
        """Return distance to a given coordinate

        """
        dx = x - self.x
        dy = y - self.y
        return math.sqrt(dx**2 + dy**2)

    def draw(self):
        """Draw the character at this position

        """
        console.draw_char(
            self.x, self.y, self.char,
            fg=self.color, bg=None
        )

    def clear(self):
        """Clear the character at this position

        """
        console.draw_char(self.x, self.y, ' ', self.color, bg=None)

    def compute_FOV(self):
        """Computes the current FOV based on the current player position

        """
        if self.dungeon:
            self.visible_tiles = tdl.map.quickFOV(
                self.x, self.y,
                self.dungeon.map_manager.is_visible_tile,
                fov=settings.FOV_ALGO,
                radius=settings.FOV_TORCH_RADIUS,
                lightWalls=settings.FOV_LIGHT_WALLS
            )
        else:
            log.warn('Failed to compute FOV for {}: Dungeon not set!'.format(
                self.name
            ))
