import logging

from rogue.utils import colors


log = logging.getLogger('default')


class FighterComponent:
    """Combat related methods for entities

    """
    def __init__(self, hp, defense, power, xp, death_handler=None):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.xp = xp
        self.death_handler = death_handler

    @property
    def power(self):
        bonus = 0
        if hasattr(self.owner, 'get_all_equipped'):
            bonus = sum(e.power_bonus or 0
                        for e in self.owner.get_all_equipped())
        return self.base_power + bonus

    @property
    def defense(self):
        bonus = 0
        if hasattr(self.owner, 'get_all_equipped'):
            bonus = sum(e.defense_bonus or 0
                        for e in self.owner.get_all_equipped())
        return self.base_defense + bonus

    @property
    def max_hp(self):
        bonus = 0
        if hasattr(self.owner, 'get_all_equipped'):
            bonus = sum(e.max_hp_bonus or 0
                        for e in self.owner.get_all_equipped())
        return self.base_max_hp + bonus

    def attack(self, target):
        entity = self.owner
        damage = self.power - target.fighter.defense

        if damage > 0:
            target.fighter.take_damage(damage)
        else:
            msg = '{} attempts to attack {} but it has no effect!'.format(
                entity.name.title(), target.name.title()
            )
            self.owner.dungeon.world.message(msg, colors.gray)

    def take_damage(self, damage):
        entity = self.owner
        player = entity.dungeon.world.player
        if damage > 0:
            self.hp -= damage
            msg = '{} took {} damage!'.format(entity.name.title(), damage)
            self.owner.dungeon.world.message(msg, colors.light_red)
        if self.hp <= 0 and self.death_handler:
            if entity != player:
                # Yield the player XP from killing the monster
                player.fighter.xp += self.xp
            self.death_handler(self.owner)

    def heal(self, amount):
        heal_value = self.hp + amount
        if heal_value >= self.max_hp:
            self.hp = self.max_hp
        else:
            self.hp += amount
