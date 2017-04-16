import logging
import sys

from rogue.handlers.status import ENTITY_STATUS
from rogue.utils.controls import get_move_direction, get_move_amount


log = logging.getLogger('default')


def process(dungeon):
    for ent in dungeon.entities.monsters:
        if ent.status != ENTITY_STATUS.DEAD:
            ent.ai.take_turn()
