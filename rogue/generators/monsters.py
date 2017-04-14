import logging
from random import randint

from rogue import settings
from rogue.entities.generic import GameObject
from rogue.utils import colors


log = logging.getLogger('default')


def generate(dungeon):
    """Put a monster in a room

    """
    for idx, room in enumerate(dungeon.rooms):
        num_monsters = randint(0, settings.ROOM_MAX_MONSTERS)
        log.debug('Generating {} monsters in room {}'.format(
            num_monsters, idx+1
        ))
        for i in range(num_monsters):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
            chance = randint(0, 100)
            if chance < 80:
                # create an orc
                obj = GameObject(
                    x, y, 'o', 'Orc',
                    colors.desaturated_green,
                    blocks=True
                )
            else:
                # create a troll
                obj = GameObject(
                    x, y, 'T', 'Troll',
                    colors.darker_green,
                    blocks=True
                )
            dungeon.entities.add('monster', obj)
