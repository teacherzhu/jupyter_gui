from os import environ
from os.path import join

from .taskmanager import TaskManager
from .support import load_config, load_libraries, check_jsons

# ======================================================================================================================
# Set up environment
# ======================================================================================================================
HOME_DIR = environ['HOME']
SIMPLEX_DIR = join(HOME_DIR, 'simplex/')

SIMPLEX_DATA_DIR = join(SIMPLEX_DIR, 'simplex_data/')
SIMPLEX_LIBRARIES = load_libraries(SIMPLEX_DATA_DIR)

SIMPLEX_CONFIG_FILE = join(SIMPLEX_DIR, 'config.sh')
SIMPLEX_CONFIG = load_config(SIMPLEX_CONFIG_FILE)

check_jsons(SIMPLEX_LIBRARIES)


# ======================================================================================================================
# Set up Jupyter widget
# ======================================================================================================================

# TODO: understand better
def _jupyter_nbextension_paths():
    """
    Required function to add things to the nbextension path.
    :return: list; List of 1 dictionary
    """

    # section: the path is relative to the simplex/ directory (if viewing from the repository: it's simplex/simplex/)
    # dest: Jupyter sets up: server(such as localhost:8888)/nbextensions/dest/
    # src: Jupyter sees this directory (not all files however) when it looks at dest (server/nbextensions/dest/)
    # require: Jupyter loads this file; things in this javascript will be seen
    # in the javascript namespace
    to_return = {'section': 'notebook', 'src': 'static',
                 'dest': 'simplex', 'require': 'simplex/main'}

    return [to_return]


def _jupyter_server_extension_paths():
    """
    Required function to add things to the server extension path.
    :return: list; List of 1 dictionary
    """

    # module:
    to_return = {'module': 'simplex'}
    return [to_return]


# TODO: understand better
def load_jupyter_server_extension(nbapp):
    """
    Function to be called when server extension is loaded.
    :param nbapp: NotebookWebApplication; handle to the Notebook webserver instance
    :return: None
    """

    # Print statement to show extension is loaded
    nbapp.log.info('----- SimpleX On -----')
