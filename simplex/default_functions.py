from os import remove, symlink
from os.path import join, split

from . import SIMPLEX_JSON_DIR


def link_simplex_json(filepath):
    """
    Soft link filepath to $HOME/.SimpleX/json/ directory.
    :param filepath: str;
    :return: None
    """

    dest = join(SIMPLEX_JSON_DIR, split(filepath)[1])
    remove(dest)
    symlink(filepath, dest)
