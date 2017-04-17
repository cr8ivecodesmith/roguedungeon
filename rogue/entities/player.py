from rogue.entities.components.fighters import FighterComponent
from rogue.entities.generic import GameObject
from rogue.handlers.death import player_death
from rogue.utils import colors


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
