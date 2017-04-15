import logging
import sys

from rogue.utils.controls import get_move_direction, get_move_amount


log = logging.getLogger('default')

DO_NOTHING = 'no-action'
DO_SKIP = 'skip'
DO_FIGHT = 'fight'
DO_MOVE = 'move'


class PlayerAction:
    def __init__(self, dungeon, user_input):
        self.dungeon = dungeon
        self.user_input = user_input
        self.player = dungeon.entities.player
        self._action = None

        direction = get_move_direction(self.user_input)
        if direction:
            self.move_or_attack(direction)
        else:
            self.do_other_action()

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, val):
        self._action = val

    def move_or_attack(self, direction):
        move_amount = get_move_amount(direction)
        x, y = self.player.x + move_amount[0], self.player.y + move_amount[1]

        target = None
        for ent in self.dungeon.entities.all(iterator=True):
            if ent.x == x and ent.y == y:
                target = ent
                break

        if target:
            self.player.fighter.attack(target)
            self.action = DO_FIGHT
        else:
            self.player.move(*move_amount)
            log.debug('Player has moved [{}] from {} to {}'.format(
                self.player.has_moved(),
                (self.player.prev_x, self.player.prev_y),
                (self.player.x, self.player.y)
            ))
            self.action = DO_MOVE

    def do_other_action(self):
        self.action = DO_NOTHING


def process(user_input, dungeon):
    if not user_input:
        return
    p_action = PlayerAction(dungeon, user_input)
    return p_action.action
