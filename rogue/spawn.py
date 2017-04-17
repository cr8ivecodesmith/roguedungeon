import logging
from random import randint

from rogue import settings
from rogue.entities.components.fighters import FighterComponent
from rogue.entities.components.monsters import BasicMonsterAIComponent
from rogue.entities.generic import GameObject
from rogue.entities.player import Player
from rogue.handlers.death import monster_death
from rogue.utils import colors


log = logging.getLogger('default')


def spawn_player(gameworld, dungeon):
    """Initializes the player on the first room

    """
    player = Player(world=gameworld)
    gameworld.player = player
    player.dungeon = dungeon
    player.x, player.y = dungeon.rooms[0].center()
    log.debug('{} placed at {}'.format(player.name, (player.x, player.y)))


def spawn_monsters(dungeon):
    """Spawn dungeon monsters

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
                fighter_component = FighterComponent(
                    hp=10, defense=0, power=3,
                    death_handler=monster_death
                )
                ai_component = BasicMonsterAIComponent()
                obj = GameObject(
                    x, y, 'o', 'Orc',
                    colors.desaturated_green,
                    blocks=True,
                    fighter=fighter_component, ai=ai_component
                )
            else:
                # create a troll
                fighter_component = FighterComponent(
                    hp=16, defense=1, power=4,
                    death_handler=monster_death
                )
                ai_component = BasicMonsterAIComponent()
                obj = GameObject(
                    x, y, 'T', 'Troll',
                    colors.darker_green,
                    blocks=True,
                    fighter=fighter_component, ai=ai_component
                )
            dungeon.entities.add('monster', obj)
