import os
import json


def load_config(filepath):
    """

    :param filepath:
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

    :param directory_path:
    :return:
    """

    libs = []
    for f in os.listdir(directory_path):
        fp = os.path.join(directory_path, f)
        if os.path.isdir(fp):
            libs.append(fp)
    libs = sorted(libs)

    print('Simple libraries:')
    for lib in libs:
        print('\t{}'.format(lib))

    return libs


def check_jsons(directory_paths):
    for dp in directory_paths:
        lib = os.path.split(dp)[1]

        fp_json = os.path.join(dp, '{}.json'.format(lib))
        try:
            load_json(fp_json)
        except FileNotFoundError:
            raise FileNotFoundError('{} library is missing {}.json.'.format(dp, lib))
        except KeyError:
            raise ValueError('Error loading {}.'.format(fp_json))
    else:
        print('All .json files are good.')


def load_json(filepath, directory_path=SIMPLEX_DATA_DIR):
    """

    :param filepath:
    :param directory_path:
    :return:
    """

    # Open .json
    with open(filepath) as f:
        library = json.load(f)

    processed_tasks = {}

    # Library name
    library_name = library['library_name']

    # Library path
    if 'library_path' in library:
        library_path = library['library_path']
    else:
        library_path = os.path.join(directory_path, library_name, '')
        print('No library path is specified for {} library so guessed to be {}.'.format(library_name, library_path))
    if not library_path.endswith('/'):
        library_path += '/'
        print('Appended \'/\' to library_path, which is now: {}.'.format(library_path))
    if not os.path.isdir(library_path):
        library_path = os.path.join(filepath.split(library_path)[0], library_path)
        if not os.path.isdir(library_path):
            raise ValueError('Error converting the library path {} to the absolute path.'.format(library_path))

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
