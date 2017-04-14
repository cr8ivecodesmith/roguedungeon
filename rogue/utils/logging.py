import os

from logging import config

from rogue import settings


def setup():
    if not os.path.isdir(settings.LOGDIR):
        os.mkdir(settings.LOGDIR)
    if not os.path.exists(settings.LOGFILE):
        with open(settings.LOGFILE, 'w') as fh:
            fh.close()
    config.dictConfig(settings.LOGGING)
