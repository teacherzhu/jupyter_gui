from os import environ
from os.path import join, dirname, realpath

from .support import establish_filepath

# ======================================================================================================================
# Set up Simpli
# ======================================================================================================================
try:
    HOME_DIR = environ['HOME']

except KeyError:  # For Windows
    HOME_DIR = environ['HOMEPATH']

SIMPLI_DIR = join(HOME_DIR, '.Simpli')
SIMPLI_JSON_DIR = join(SIMPLI_DIR, 'json', '')
SIMPLI_TASK_RECORD_FILEPATH = join(SIMPLI_JSON_DIR, 'COMPILED.json')

THIS_DIR = dirname(realpath(__file__))

from .default_apps import *
from .taskmanager import TaskManager, compile_tasks

establish_filepath(SIMPLI_DIR)
establish_filepath(SIMPLI_JSON_DIR)
link_simpli_json(join(THIS_DIR, 'simpli.json'))


# ======================================================================================================================
# Set up Jupyter widget
# ======================================================================================================================
# TODO: understand better


def _jupyter_nbextension_paths():
    """
    Required function to add things to the nbextension path.
    :return: list; List of 1 dictionary
    """

    # section: the path is relative to the simpli/ directory (if viewing from the repository: it's simpli/simpli/)
    # dest: Jupyter sets up: server(such as localhost:8888)/nbextensions/dest/
    # src: Jupyter sees this directory (not all files however) when it looks at dest (server/nbextensions/dest/)
    # require: Jupyter loads this file; things in this javascript will be seen
    # in the javascript namespace
    to_return = {'section': 'notebook', 'src': 'static', 'dest': 'simpli', 'require': 'simpli/main'}

    return [to_return]


def _jupyter_server_extension_paths():
    """
    Required function to add things to the server extension path.
    :return: list; List of 1 dictionary
    """

    # module:
    to_return = {'module': 'simpli'}
    return [to_return]


# TODO: understand better
def load_jupyter_server_extension(nbapp):
    """
    Function to be called when server extension is loaded.
    :param nbapp: NotebookWebApplication; handle to the Notebook web-server instance
    :return: None
    """

    # Print statement to show extension is loaded
    nbapp.log.info('----- Simpli On -----')
