import logging


log = logging.getLogger('default')


class FighterComponent:
    """Combat related methods for entities

    """
    def __init__(self, hp, defense, power, death_handler=None):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.death_handler = death_handler

    def attack(self, target):
        entity = self.owner
        damage = self.power - target.fighter.defense

        if damage > 0:
            target.fighter.take_damage(damage)
        else:
            msg = '{} attempts to attack {} but it has no effect!'.format(
                entity.name.title(), target.name.title()
            )
            self.owner.dungeon.world.message(msg)

    def take_damage(self, damage):
        entity = self.owner
        if damage > 0:
            self.hp -= damage
            msg = '{} took {} damage!'.format(entity.name.title(), damage)
            self.owner.dungeon.world.message(msg)
        if self.hp <= 0 and self.death_handler:
            self.death_handler(self.owner)

    def heal(self, amount):
        heal_value = self.hp + amount
        if heal_value >= self.max_hp:
            self.hp = self.max_hp
        else:
            self.hp += amount
