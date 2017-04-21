from rogue.consoles import tdl
from rogue.entities.components.fighters import FighterComponent
from rogue.entities.generic import GameObject
from rogue.handlers.death import player_death
from rogue.utils import colors
from rogue.utils.controls import get_clicked_coords


class Player(GameObject):
    __world = None
    inventory = []
    equipment = {
        'right_hand': None,
        'left_hand': None,
        'body': None,
    }

    def __init__(
        self, name=None, x=0, y=0,
        world=None, **kwargs
    ):
        name = name or 'Stranger'
        char, color = '@', colors.white
        blocks = True
        fighter_component = FighterComponent(
            hp=30, defense=2, power=5,
            death_handler=player_death
        )

        super(Player, self).__init__(
            x=x, y=y,
            char=char, name=name, color=color,
            blocks=blocks, fighter=fighter_component,
            **kwargs
        )

        self.world = world

    @property
    def world(self):
        return self.__world

    @world.setter
    def world(self, val):
        self.__world = val
        self.__world.player = self

    def closest_monster(self, max_range=0):
        """Find the closest monster within FOV

        """
        monsters = self.dungeon.entities.monsters
        closest_enemy = None
        closest_dist = max_range + 1  # start with (slightly more) max range.

        for obj in monsters:
            if obj.fighter and obj.coords() in self.visible_tiles:
                dist = self.distance_to(obj)
                if dist < closest_dist:
                    closest_enemy = obj
                    closest_dist = dist
        return closest_enemy

    def target_tile(self, max_range=None):
        """Return the clicked tile coordinates within FOV
        The screen needs to be updated while the player is still selecting
        targets.

        """
        coords = (None, None)
        while True:
            tdl.flush()
            coords = get_clicked_coords()
            if coords == (None, None):
                break
            self.world.render.all()
            if (
                coords in self.visible_tiles and
                (max_range is None or self.distance(*coords) <= max_range)
            ):
                break
        return coords

    def target_monster(self, max_range=None):
        """Return the clicked monster instance within FOV

        """
        monsters = self.dungeon.entities.monsters
        while True:
            x, y = self.target_tile(max_range)
            if x is None:
                return None
            for obj in monsters:
                if obj.coords() == (x, y) and obj.fighter:
                    return obj
