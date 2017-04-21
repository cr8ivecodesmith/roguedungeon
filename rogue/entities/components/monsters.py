import logging
from random import randint

from rogue import settings
from rogue.utils import colors


log = logging.getLogger('default')


class BasicMonsterAIComponent:
    def take_turn(self):
        monster = self.owner
        dungeon = monster.dungeon
        player = dungeon.world.player
        visible_tiles = player.visible_tiles

        if monster.coords() in visible_tiles:
            # move towards the player
            msg = 'The {} moves toward you.'.format(
                monster.name.title()
            )
            dungeon.world.message(msg)

            if monster.distance_to(player) >= 2:
                monster.move_towards(player.x, player.y)
            elif player.fighter.hp > 0:
                monster.fighter.attack(player)


class ConfusedMonsterAIComponent:
    def __init__(self, old_ai, num_turns=settings.SPELL_CONFUSE_NUM_TURNS):
        self.old_ai = old_ai
        self.num_turns = num_turns

    def take_turn(self):
        monster = self.owner
        world = monster.dungeon.world

        if self.num_turns > 0:
            # Still confused; move in random direction and decrease confuse
            # turns
            monster.move(
                randint(-1, 1),
                randint(-1, 1)
            )
            self.num_turns -= 1
        else:
            # Restore old AI
            self.owner.ai = self.old_ai
            world.message(
                'The {} is no longer confused!'.format(self.owner.name),
                colors.red
            )
