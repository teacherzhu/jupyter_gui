from os import remove, symlink
from os.path import join, split, islink

from . import SIMPLEX_JSON_DIR


def link_simplex_json(filepath):
    """
    Soft link filepath to $HOME/.SimpleX/json/ directory.
    :param filepath: str;
    :return: None
    """

    dest = join(SIMPLEX_JSON_DIR, split(filepath)[1])
    if islink(dest):
        remove(dest)
    symlink(filepath, dest)


def reset_simplex_json():
    """
    Delete all files in $HOME/.SimpleX/json/ directory.
    :param filepath: str;
    :return: None
    """

    # TODO: implement
