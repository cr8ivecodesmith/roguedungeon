import os
from random import choice

from rogue import settings


def get_noun_list():
    words = []
    wfile = os.path.join(settings.DATADIR, 'wordlists', 'nouns.list')
    with open(wfile, 'r') as fh:
        for line in fh:
            line = line.strip()
            if line and not line.startswith('#'):
                words.append(line)
    return words


def get_adjective_list():
    words = []
    wfile = os.path.join(settings.DATADIR, 'wordlists', 'adjectives.list')
    with open(wfile, 'r') as fh:
        for line in fh:
            line = line.strip()
            if line and not line.startswith('#'):
                words.append(line)
    return words


def random_name(*word_lists):
    word_lists = word_lists or [get_adjective_list, get_noun_list]
    name = [choice(l()) for l in word_lists]
    return ' '.join(name)
