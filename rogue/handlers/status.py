from collections import namedtuple

_entity_status = namedtuple('_entity_status', ' '.join([
    'NO_ACTION',
    'SKIP_TURN',
    'MOVE',
    'FIGHT',
    'DEAD',
]))


_game_status = namedtuple('_game_status', ' '.join([
    'PLAY',
    'QUIT',
]))


ENTITY_STATUS = _entity_status(
    NO_ACTION=0,
    SKIP_TURN=1,
    MOVE=2,
    FIGHT=3,
    DEAD=4
)


GAME_STATUS = _game_status(
    PLAY=0,
    QUIT=1,
)
