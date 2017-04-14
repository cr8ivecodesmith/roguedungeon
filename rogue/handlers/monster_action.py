import logging
import sys

from rogue.utils.controls import get_move_direction, get_move_amount


log = logging.getLogger('default')


def process(dungeon):
    for ent in dungeon.entities.monsters:
        log.info('The {} growls!'.format(ent.name.title()))
