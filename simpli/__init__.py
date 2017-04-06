from os.path import dirname, join, realpath

from .default_tasks import link_json
from .support import establish_filepath, get_home_dir

# ==============================================================================
# Link default JSON to ~/.simpli/json
# ==============================================================================
# Make a hidden directory in the user-home directory
HOME_DIR = get_home_dir()
SIMPLI_DIR = join(HOME_DIR, '.simpli')
SIMPLI_JSON_DIR = join(SIMPLI_DIR, 'json/')
establish_filepath(SIMPLI_JSON_DIR)

link_json(join(dirname(realpath(__file__)), 'default_tasks.json'))


# ==============================================================================
# Set up Jupyter Notebook extension
# ==============================================================================
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
    to_return = {
        'section': 'notebook',
        'src': 'static',
        'dest': 'simpli',
        'require': 'simpli/main',
    }

    return [to_return]


def _jupyter_server_extension_paths():
    """
    Required function to add things to the server extension path.
    :return: list; List of 1 dictionary
    """

    to_return = {
        'module': 'simpli',
    }
    return [to_return]


def load_jupyter_server_extension(nbapp):
    """
    Function to be called when server extension is loaded.
    :param nbapp: NotebookWebApplication; handle to the Notebook web-server instance
    :return: None
    """

    # Print statement to show extension is loaded
    nbapp.log.info('********* Simpli On *********')
