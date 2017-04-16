from rogue.generators.name import random_name
from rogue.handlers.status import GAME_STATUS
from rogue.worlds.dungeon import Dungeon


class GameWorld:
    def __init__(self):
        self.status = GAME_STATUS.PLAY
        self.dungeons = []
        self.current_dungeon = None

    def generate_dungeon(self, current=False):
        depth = 0 if not self.dungeons else len(self.dungeons)
        name = (random_name()).title()
        dungeon = Dungeon(world=self, name=name, depth=depth)
        self.dungeons.append(dungeon)
        if current:
            self.current_dungeon = dungeon
        return dungeon
