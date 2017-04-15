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
        log.info('{} attempts to attack {}'.format(
            entity.name.title(), target.name.title()
        ))

