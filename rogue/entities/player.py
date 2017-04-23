from rogue import settings
from rogue.consoles import tdl, root_console, console
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
        self, name=None, x=0, y=0, level=1,
        world=None, **kwargs
    ):
        name = name or 'Stranger'
        char, color = '@', colors.white
        blocks = True
        fighter_component = FighterComponent(
            hp=30, defense=2, power=5, xp=0,
            death_handler=player_death
        )
        self.level = level

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

    @property
    def next_level_xp(self):
        return (
            settings.PLAYER_LEVEL_UP_BASE +
            (self.level * settings.PLAYER_LEVEL_UP_FACTOR)
        )

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

    def move_downstairs(self):
        """Move the player to the next dungeon and put him at the center
        of the first room

        """
        downstairs = self.dungeon.stairs.get('DOWN')
        valid = (
            len(self.world.dungeons) > 1 and
            downstairs and
            downstairs.coords() in self.visible_tiles
        )
        if valid:
            d_idx = self.world.dungeons.index(self.dungeon)
            self.dungeon = self.world.dungeons[d_idx + 1]

            self.x, self.y = self.dungeon.rooms[0].center()

            root_console.clear()
            console.clear()
            self.world.render.all()

    def move_upstairs(self):
        """Move the player to the previous dungeon and put him at the center
        of the last room

        """
        upstairs = self.dungeon.stairs.get('UP')
        valid = (
            self.dungeon.depth > 1 and
            len(self.world.dungeons) > 1 and
            upstairs and
            upstairs.coords() in self.visible_tiles
        )
        if valid:
            d_idx = self.world.dungeons.index(self.dungeon)
            self.dungeon = self.world.dungeons[d_idx - 1]

            self.x, self.y = self.dungeon.rooms[-1].center()

            root_console.clear()
            console.clear()
            self.world.render.all()

    def check_level_up(self):
        if self.fighter.xp < self.next_level_xp:
            return

        self.level += 1
        self.fighter.xp = 0
        self.world.message(
            'Your battle skills grow stronger. You reached level {}!'.format(
                self.level
            ),
            colors.yellow,
            force_render=True
        )

        choice = None
        while choice is None:
            choice = self.world.render.menu(
                'Level up! Coose stat to raise.\n', [
                    'Constitution (+20HP from {})'.format(self.fighter.max_hp),
                    'Strength (+1atk from {})'.format(self.fighter.power),
                    'Agility (+1def from {})'.format(self.fighter.defense),
                ], settings.LEVEL_SCREEN_WIDTH)
        if choice == 0:
            self.fighter.max_hp += 20
            self.fighter.hp += 20
        elif choice == 1:
            self.fighter.power += 1
        elif choice == 2:
            self.fighter.defense += 1
