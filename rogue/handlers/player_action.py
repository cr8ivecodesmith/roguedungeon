import logging
import sys

from rogue.utils.controls import get_move_direction, get_move_amount
from rogue.handlers.status import ENTITY_STATUS


log = logging.getLogger('default')


class PlayerAction:
    def __init__(self, gameworld, user_input):
        self.dungeon = gameworld.current_dungeon
        self.user_input = user_input
        self.player = self.dungeon.entities.player

        direction = get_move_direction(self.user_input)
        if direction:
            self.move_or_attack(direction)
        else:
            self.do_other_action()

    def move_or_attack(self, direction):
        move_amount = get_move_amount(direction)
        x, y = self.player.x + move_amount[0], self.player.y + move_amount[1]

        target = None
        for ent in self.dungeon.entities.all(iterator=True):
            if ent.fighter and ent.x == x and ent.y == y:
                target = ent
                break

        if target:
            self.player.fighter.attack(target)
            self.player.status = ENTITY_STATUS.FIGHT
        else:
            self.player.move(*move_amount)
            log.debug('Player has moved [{}] from {} to {}'.format(
                self.player.has_moved(),
                (self.player.prev_x, self.player.prev_y),
                (self.player.x, self.player.y)
            ))
            self.player.status = ENTITY_STATUS.MOVE

    def do_other_action(self):
        self.player.status = ENTITY_STATUS.NO_ACTION


def process(user_input, gameworld):
    if not user_input:
        return
    PlayerAction(gameworld, user_input)
    return
