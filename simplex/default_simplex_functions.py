from os import remove, symlink
from os.path import join, split, islink

from IPython.core.display import display_html

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
