"""
Defines default tasks, which are generally useful.
"""

from os import listdir, remove, symlink
from os.path import islink, join, split

from IPython.core.display import display_html

from . import SIMPLI_JSON_DIR


def just_return(value):
    """
    Just return.
    :param value:
    :return: obj
    """

    return value


def slice_dataframe(dataframe, indices=(), ax=0):
    """
    Slice dataframe.
    :param dataframe: dataframe;
    :param indices: iterable;
    :param ax: int;
    :return: dataframe;
    """

    if isinstance(indices, str):
        indices = [indices]

    if ax == 0:
        return dataframe.ix[indices, :]
    elif ax == 1:
        return dataframe.ix[:, indices]


# ==============================================================================
# JSON
# ==============================================================================
def link_json(filepath):
    """
    Soft link JSON filepath to $HOME/.simpli/json/ directory.
    :param filepath: str; JSON filepath
    :return: None
    """

    destination = join(SIMPLI_JSON_DIR, split(filepath)[1])
    if islink(destination):
        remove(destination)
    symlink(filepath, destination)


def reset_jsons():
    """
    Delete all files except default_tasks.json in $HOME/.simpli/json/ directory.
    :return: None
    """

    for f in listdir(SIMPLI_JSON_DIR):
        if f != 'default_tasks.json':
            remove(join(SIMPLI_JSON_DIR, f))


# ==============================================================================
# HTML
# ==============================================================================
def set_notebook_theme(filepath):
    """
    Set notebooks theme.
    :param filepath: str; .css
    :return: None
    """

    html = """<style> {} </style>""".format(open(filepath, 'r').read())
    display_raw_html(html)


def display_raw_html(html, hide_input_cell=True):
    """
    Execute raw HTML.
    :param html: str; HTML
    :param hide_input_cell: bool;
    :return: None
    """

    if hide_input_cell:
        html += """<script> $('div .input').hide()"""
    display_html(html, raw=True)
