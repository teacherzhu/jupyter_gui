from os import environ, listdir
from os.path import join, split, isfile, isdir
import json

from .taskmanager import TaskManager


# ======================================================================================================================
# Set up environment
# ======================================================================================================================
def load_config(filepath):
    """

    :param filepath: str; config.txt
    :return:
    """

    config = {}
    with open(filepath) as f:
        for line in f:
            k, v = line.strip().split('=')
            config[k] = v

    print('Simplex configuration:')
    for k, v in sorted(config.items()):
        print('\t{} : {}'.format(k, v))

    return config


def load_libraries(directory_path):
    """

    :param directory_path: str; simplex_data directory
    :return: list; list of library directory paths
    """

    libs = []
    for f in listdir(directory_path):
        fp = join(directory_path, f)
        if isdir(fp):
            libs.append(fp)
    libs = sorted(libs)

    print('Simple libraries:')
    for lib in libs:
        print('\t{}'.format(lib))

    return libs


def check_jsons(directory_paths):
    """

    :param directory_paths: list; list of library directory paths
    :return: None
    """

    for dp in directory_paths:
        lib = split(dp)[1]

        fp_json = join(dp, '{}.json'.format(lib))
        try:
            load_json(fp_json)
        except FileNotFoundError:
            raise FileNotFoundError('{} library is missing {}.json.'.format(dp, lib))
        except KeyError:
            raise ValueError('Error loading {}.'.format(fp_json))
    else:
        print('All .json files are good.')


def load_json(filepath):
    """

    :param filepath: str; full path to library.json
    :return: None
    """

    if isfile(filepath):
        raise FileNotFoundError('The file {} isn\'t found or isn\'t an absolute path.')

    # Open .json
    with open(filepath) as f:
        library = json.load(f)

    processed_tasks = {}

    # Library name
    library_name = library['library_name']

    # Library path
    if 'library_path' in library:
        library_path = library['library_path']
        if not library_path.endswith('/'):
            library_path += '/'
            print('Appended \'/\' to library_path, which is now: {}.'.format(library_path))
    else:
        library_path = join(split(filepath)[0], '')
        print('No library path is specified for {} library so guessed to be {}.'.format(library_name, library_path))
    if not isdir(library_path):
        library_path = join(HOME_DIR, library_path)
        print('Converted the library path {} to the absolute path relative to $HOME directory.'.format(library_path))

    # Tasks
    tasks = library['tasks']
    for task in tasks:

        # Task label is this task's UID
        label = task['label']
        if label in processed_tasks:
            raise ValueError('Multiple \'{}\' task labels found! Use unique task label for each task.'.format(label))
        else:
            processed_tasks[label] = {}

        # Function name
        processed_tasks[label]['function_name'] = task['function_name']

        # Description
        if 'description' in task:
            processed_tasks[label]['description'] = task['description']

        # Arguments
        if 'required_args' in task:
            processed_tasks[label]['required_args'] = task['required_args']
        if 'optional_args' in task:
            processed_tasks[label]['optional_args'] = task['optional_args']
        if 'default_args' in task:
            processed_tasks[label]['default_args'] = task['default_args']

        # Returns
        if 'returns' in task:
            processed_tasks[label]['returns'] = task['returns']

    return processed_tasks


HOME_DIR = environ['HOME']
SIMPLEX_DIR = join(HOME_DIR, 'simplex/')

SIMPLEX_CONFIG_FILE = join(SIMPLEX_DIR, 'config.sh')
SIMPLEX_CONFIG = load_config(SIMPLEX_CONFIG_FILE)

SIMPLEX_DATA_DIR = join(SIMPLEX_DIR, 'simplex_data/')
SIMPLEX_LIBRARIES = load_libraries(SIMPLEX_DATA_DIR)

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
