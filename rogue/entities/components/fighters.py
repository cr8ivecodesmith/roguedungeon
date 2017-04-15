import logging


log = logging.getLogger('default')


class FighterComponent:
    """Combat related methods for entities

    """
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power

    def attack(self, target):
        entity = self.owner
        damage = self.power - target.fighter.defense

        if damage > 0:
            target.fighter.take_damage(damage)
        else:
            log.info('{} attempts to attack {} but it has no effect!'.format(
                entity.name.title(), target.name.title()
            ))

    def take_damage(self, damage):
        # TODO: Handle death
        entity = self.owner
        if damage > 0:
            self.hp -= damage
            log.info('{} took {} damage!'.format(entity.name.title(), damage))
