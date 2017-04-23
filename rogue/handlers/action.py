import logging

from rogue.handlers.status import ENTITY_STATUS, GAME_STATUS
from rogue.spawn import spawn_next_level
from rogue.utils.controls import get_move_direction, get_move_amount


log = logging.getLogger('default')


def monster_action(world):
    """Process the monster actions

    Process monster action only when the game is still on play and when the
    player took an action.

    """
    player = world.player
    dungeon = player.dungeon
    if (
        world.status == GAME_STATUS.PLAY and
        player.status != ENTITY_STATUS.NO_ACTION
    ):
        for ent in dungeon.entities.monsters:
            if ent.status != ENTITY_STATUS.DEAD and ent.ai:
                ent.ai.take_turn()


def player_other_action(user_input, world):
    """Process other actions based on the the input

    This function updates the player status

    """
    player = world.player
    dungeon = player.dungeon

    player.status = ENTITY_STATUS.NO_ACTION

    log.debug(user_input)

    if (user_input.key == 'CHAR' and user_input.char == 'g'):
        for loot in dungeon.entities.loot:
            if loot.coords() == player.coords():
                loot.item.pick_up()
                player.status = ENTITY_STATUS.PICK
                break
    elif (user_input.key == 'CHAR' and user_input.char == 'i'):
        chosen_item = world.render.inventory_menu()
        if chosen_item:
            chosen_item.use()
            player.status = ENTITY_STATUS.USE
    elif (user_input.key == 'CHAR' and user_input.char == 'd'):
        chosen_item = world.render.inventory_menu(drop=True)
        if chosen_item:
            chosen_item.drop()
            player.status = ENTITY_STATUS.USE
    elif (user_input.key == 'CHAR' and user_input.char == 'c'):
        info = (
            'Some long character info\n\n'
            'goes here...'
        )
        world.message_box(info)
    elif (user_input.key == 'TEXT' and user_input.text == '<'):
        spawn_next_level(world)
        player.move_downstairs()
    elif (user_input.key == 'TEXT' and user_input.text == '>'):
        player.move_upstairs()


def player_move_or_attack(user_input, world):
    """Either move in the specified direction or attack a target in the
    specfied direction.

    This function updates the player status

    """
    direction = get_move_direction(user_input)
    player = world.player
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


def player_action(user_input, world):
    """Process the player actions

    """
    player = world.player

    if not user_input:
        player.status = ENTITY_STATUS.NO_ACTION
        return

    direction = get_move_direction(user_input)
    if direction:
        player_move_or_attack(user_input, world)
    else:
        player_other_action(user_input, world)
