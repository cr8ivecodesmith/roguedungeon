import logging


log = logging.getLogger('default')


class BasicMonsterAIComponent:
    def take_turn(self):
        monster = self.owner
        dungeon = monster.dungeon
        player = dungeon.world.player
        visible_tiles = player.visible_tiles

        if (monster.x, monster.y) in visible_tiles:
            # move towards the player
            msg = 'The {} moves toward you.'.format(
                monster.name.title()
            )
            dungeon.world.message(msg)

            if monster.distance_to(player) >= 2:
                monster.move_towards(player.x, player.y)
            elif player.fighter.hp > 0:
                monster.fighter.attack(player)
