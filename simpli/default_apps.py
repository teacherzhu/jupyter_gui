from os import remove, symlink
from os.path import join, split, islink

from IPython.core.display import display_html

from . import SIMPLI_JSON_DIR


def link_simpli_json(filepath):
    """
    Soft link filepath to $HOME/.Simpli/json/ directory.
    :param filepath: str;
    :return: None
    """

    dest = join(SIMPLI_JSON_DIR, split(filepath)[1])
    if islink(dest):
        remove(dest)
    symlink(filepath, dest)


def reset_simpli_json():
    """
    Delete all files in $HOME/.Simpli/json/ directory.
    :param filepath: str;
    :return: None
    """

    # TODO: implement


def youtube(url):
    """

    :param url:
    :return:
    """

    url = url.replace('/watch?v=', '/embed/')
    html = '<iframe width="560" height="315" src="{}" frameborder="0" allowfullscreen></iframe>'.format(url)
    display_raw_html(html)


def set_theme(filepath):
    """

    :param filepath: str; .css
    :return: None
    """

    html = '<style> {} </style>'.format(open(filepath, 'r').read())
    display_raw_html(html)


def display_raw_html(html):
    """
    Execute raw HTML.
    :param html: str; HTML
    :return: None
    """

    # print('display_raw_html: {}'.format(html))
    display_html(html, raw=True)


def just_return(item):
    """
    :param item:
    :return:
    """
    return item


def slice_dataframe(dataframe, indices=(), ax=0):
    """

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
