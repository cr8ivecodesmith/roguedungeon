from random import randint


def random_choice_index(chances):
    """Determine where in the list the random choice lands and return the
    corresponding index.

    """
    dice = randint(0, sum(chances))

    running_sum = 0
    for idx, value in enumerate(chances):
        running_sum += value
        if dice <= running_sum:
            return idx


def random_choice(chances_dict):
    """Pick a random item in the dictionary and return the key.

    """
    chances = chances_dict.values()
    keys = chances_dict.keys()
    return keys[random_choice_index(chances)]


def from_dungeon_level(table, depth):
    """Return a value depending on the dungeon depth.

    This is useful to determine how many occurences of an entity will appear
    given a dungeon depth.

    The table specifies what value occurs after each level, default is 0.
    The table is a list of tuples where: (value, dungeon_depth)

    """
    def key(val):
        return val[-1]

    for value, level in sorted(table, key=key):
        if depth >= level:
            return value

    return 0
