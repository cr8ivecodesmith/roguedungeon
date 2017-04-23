from rogue import settings
from rogue.utils import colors


class ItemComponent:
    def __init__(self, use_handler=None):
        self.use_handler = use_handler

    def pick_up(self):
        dungeon = self.owner.dungeon
        loot = dungeon.entities.loot
        world = dungeon.world
        player = world.player
        inventory = player.inventory

        if len(inventory) >= settings.PLAYER_MAX_INVENTORY:
            world.message('Your inventory is full, cannot pick up {}.'.format(
                          self.owner.name), colors.red)
        else:
            inventory.append(self.owner)
            loot.remove(self.owner)
            world.message('You picked up the {}!'.format(self.owner.name),
                          colors.green)

        # TODO: Implement equipment handling
        # special case: if item is an equipment, equip it if the slot is unused
        equipment = self.owner.equipment
        if equipment and not player.get_equipment_in_slot(equipment.slot):
            equipment.equip()

    def use(self):
        dungeon = self.owner.dungeon
        world = dungeon.world
        player = world.player
        inventory = player.inventory

        # Special case for equipments
        if self.owner.equipment:
            self.owner.equipment.toggle_equip()
            return

        if not self.use_handler:
            world.message('The {} cannot be used.'.format(self.owner.name))
        else:
            if self.use_handler(player):
                # destroy after use unless it was cancelled.
                inventory.remove(self.owner)
            else:
                world.message('Cancelled.', colors.red)

    def drop(self):
        dungeon = self.owner.dungeon
        loot = dungeon.entities.loot
        world = dungeon.world
        player = world.player
        inventory = player.inventory

        loot.append(self.owner)
        inventory.remove(self.owner)
        self.owner.x = player.x
        self.owner.y = player.y

        # special case for equipped equipment
        if self.owner.equipment:
            self.owner.equipment.dequip()

        world.message(
            'You dropped the {}.'.format(self.owner.name), colors.yellow
        )


class EquipmentComponent:
    """Equipment components require that an Item component is also present

    """
    def __init__(
        self, slot,
        defense_bonus=None, power_bonus=None, max_hp_bonus=None,
    ):
        self.slot = slot
        self.is_equipped = False
        self.defense_bonus = defense_bonus
        self.power_bonus = power_bonus
        self.max_hp_bonus = max_hp_bonus

    def toggle_equip(self):
        if self.is_equipped:
            self.dequip()
        else:
            self.equip()

    def equip(self):
        # TODO: Remove previously equipped item on the same slot
        owner = self.owner
        world = owner.dungeon.world
        player = world.player

        # Check if there's already something equipped on the slot, then remove
        # it.
        old_equip = player.get_equipment_in_slot(self.slot)
        if old_equip:
            old_equip.dequip()

        self.is_equipped = True
        world.message(
            'Equipped {} on {}'.format(owner.name, self.slot),
            colors.light_green
        )

    def dequip(self):
        owner = self.owner
        world = owner.dungeon.world
        self.is_equipped = False
        world.message(
            'Removed {} on {}'.format(owner.name, self.slot),
            colors.light_yellow
        )
