from os import remove, symlink
from os.path import join, split, islink
from shutil import rmtree

from IPython.core.display import display_html

from . import SIMPLI_JSON_DIR


def link_json(filepath):
    """
    Soft link filepath to $HOME/.Simpli/json/ directory.
    :param filepath: str;
    :return: None
    """

    dest = join(SIMPLI_JSON_DIR, split(filepath)[1])
    if islink(dest):
        remove(dest)
    symlink(filepath, dest)


def reset_jsons():
    """
    Delete all files in $HOME/.Simpli/json/ directory.
    :param filepath: str;
    :return: None
    """

    rmtree(SIMPLI_JSON_DIR)


def just_return(value):
    """
    Just return.
    :param value:
    :return: obj
    """

    print('Returning {} ...'.format(value))
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


# ======================================================================================================================
# HTML
# ======================================================================================================================
def set_theme(filepath):
    """
    Set notebook theme.
    :param filepath: str; .css
    :return: None
    """

    html = '''<style> {} </style>'''.format(open(filepath, 'r').read())
    display_raw_html(html)


def center_align_output_cells():
    """

    :return: None
    """

    html = ''''<style>.output {align-items: center; }</style>'''
    display_raw_html(html)


def display_banner():
    """

    :return: None
    """

    html = '''<img src="../media/start_banner.jpg" width=600 height=337>'''
    display_raw_html(html)


def youtube(url):
    """
    Embed a YouTube video.
    :param url:
    :return: None
    """

    url = url.replace('/watch?v=', '/embed/')
    html = '''<iframe width="560" height="315" src="{}" frameborder="0" allowfullscreen></iframe>'''.format(url)
    display_raw_html(html)


def toggle_input_cells():
    """
    Toggle all existing input cells.
    :return: None
    """

    html = '''
    <script>
        code_show=true;
        function toggle_input_cells() {
            if (code_show){
                $('div.input').hide();
            }
            else {
                $('div.input').show();
            }
            code_show = !code_show
        }
        $(document).ready(toggle_input_cells);
    </script>

    <form action="javascript:toggle_input_cells()"><input type="submit" value="Toggle input cells"></form>
    '''
    display_raw_html(html)


def display_raw_html(html, hide_input_cell=True):
    """
    Execute raw HTML.
    :param html: str; HTML
    :param hide_input_cell: bool;
    :return: None
    """

    if hide_input_cell:
        html += '''<script> $('div .input').hide()'''
    display_html(html, raw=True)
