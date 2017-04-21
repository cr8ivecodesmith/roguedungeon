import logging

from rogue.handlers.status import ENTITY_STATUS, GAME_STATUS
from rogue.utils.controls import get_move_direction, get_move_amount


log = logging.getLogger('default')


def monster_action(gameworld):
    """Process the monster actions

    Process monster action only when the game is still on play and when the
    player took an action.

    """
    player = gameworld.player
    dungeon = player.dungeon
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
    player = gameworld.player
    dungeon = player.dungeon

    player.status = ENTITY_STATUS.NO_ACTION

    if (user_input.key == 'CHAR' and user_input.char == 'g'):
        for loot in dungeon.entities.loot:
            if loot.coords() == player.coords():
                loot.item.pick_up()
                player.status = ENTITY_STATUS.PICK
                break
    elif (user_input.key == 'CHAR' and user_input.char == 'i'):
        chosen_item = gameworld.render.inventory_menu()
        if chosen_item:
            chosen_item.use()
            player.status = ENTITY_STATUS.USE
    elif (user_input.key == 'CHAR' and user_input.char == 'd'):
        chosen_item = gameworld.render.inventory_menu(drop=True)
        if chosen_item:
            chosen_item.drop()
            player.status = ENTITY_STATUS.USE


def player_move_or_attack(user_input, gameworld):
    """Either move in the specified direction or attack a target in the
    specfied direction.

    This function updates the player status

    """
    direction = get_move_direction(user_input)
    player = gameworld.player
    dungeon = player.dungeon
    dx, dy = get_move_amount(direction)
    x, y = player.x + dx, player.y + dy

    target = None
    for ent in dungeon.entities.monsters:
        if ent.fighter and ent.coords() == (x, y):
            target = ent
            break

    if target:
        player.fighter.attack(target)
        player.status = ENTITY_STATUS.FIGHT
    else:
        player.move(dx, dy)
        log.debug('Player has moved [{}] from {} to {}'.format(
            player.has_moved(), player.prev_coords(), player.coords()
        ))
        player.status = ENTITY_STATUS.MOVE


def player_action(user_input, gameworld):
    """Process the player actions

    """
    player = gameworld.player

    if not user_input:
        player.status = ENTITY_STATUS.NO_ACTION
        return

    direction = get_move_direction(user_input)
    if direction:
        player_move_or_attack(user_input, gameworld)
    else:
        player_other_action(user_input, gameworld)
