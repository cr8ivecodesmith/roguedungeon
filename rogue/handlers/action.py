import logging
import sys

from rogue.handlers.status import ENTITY_STATUS, GAME_STATUS
from rogue.utils.controls import get_move_direction, get_move_amount


log = logging.getLogger('default')


def monster_action(gameworld):
    """Process the monster actions

    Process monster action only when the game is still on play and when the
    player took an action.

    """
    dungeon = gameworld.current_dungeon
    player = dungeon.entities.player
    if (
        gameworld.status == GAME_STATUS.PLAY and
        player.status != ENTITY_STATUS.NO_ACTION
    ):
        for ent in dungeon.entities.monsters:
            if ent.status != ENTITY_STATUS.DEAD and ent.ai:
                ent.ai.take_turn()


def player_other_action(user_input, gameworld):
    """Process other actions based on the the input

    This function updates the player status

    """
    dungeon = gameworld.current_dungeon
    player = dungeon.entities.player
    player.status = ENTITY_STATUS.NO_ACTION


def player_move_or_attack(user_input, gameworld):
    """Either move in the specified direction or attack a target in the
    specfied direction.

    This function updates the player status

    """
    direction = get_move_direction(user_input)
    dungeon = gameworld.current_dungeon
    player = dungeon.entities.player
    dx, dy = get_move_amount(direction)
    x, y = player.x + dx, player.y + dy

    target = None
    for ent in dungeon.entities.all(iterator=True):
        if ent.fighter and ent.x == x and ent.y == y:
            target = ent
            break

    if target:
        player.fighter.attack(target)
        player.status = ENTITY_STATUS.FIGHT
    else:
        player.move(dx, dy)
        log.debug('Player has moved [{}] from {} to {}'.format(
            player.has_moved(),
            (player.prev_x, player.prev_y),
            (player.x, player.y)
        ))
        player.status = ENTITY_STATUS.MOVE


def player_action(user_input, gameworld):
    """Process the player actions

    """
    dungeon = gameworld.current_dungeon
    player = dungeon.entities.player
    if not user_input:
        player.status = ENTITY_STATUS.NO_ACTION
        return

    direction = get_move_direction(user_input)
    if direction:
        player_move_or_attack(user_input, gameworld)
    else:
        player_other_action(user_input, gameworld)
