from os import listdir
from os.path import isdir, isfile, join, split
from json import dump, dumps, load

from . import HOME_DIR, SIMPLEX_DATA_DIR, SIMPLEX_TASK_RECORD_FILEPATH


# ======================================================================================================================
# SimpleX support functions
# ======================================================================================================================
# TODO: return as only dictionary
def compile_tasks(library_directory_path=SIMPLEX_DATA_DIR, record_filepath=SIMPLEX_TASK_RECORD_FILEPATH,
                  return_type=str):
    """

    :param library_directory_path: str; the main directory that contains all library directories
    :param record_filepath: str; .json containing all available tasks' specifications
    :param return_type: type; dict or str
    :return: dict; all tasks' specifications
    """

    tasks_by_libraries = dict()
    for dp in list_only_dirs(library_directory_path):
        lib = split(dp)[1]

        fp_json = join(dp, '{}.json'.format(lib))
        try:
            tasks = load_task(fp_json)
            tasks_by_libraries.update(tasks)
        except FileNotFoundError:
            raise FileNotFoundError('{} library is missing {}.json (couldn\'t find {}).'.format(dp, lib, fp_json))
        except KeyError:
            raise ValueError('Error loading {}.'.format(fp_json))

    if record_filepath:
        if not record_filepath.endswith('.json'):
            record_filepath += '.json'
        with open(record_filepath, 'w') as f:
            dump(tasks_by_libraries, f, sort_keys=True, indent=2)

    if return_type == str:
        return dumps(tasks_by_libraries)

    elif return_type == dict:
        return tasks_by_libraries


def load_task(json_filepath):
    """

    :param json_filepath: str; absolute filepath to library.json
    :return: None
    """

    # print('Loading {} ...'.format(filepath))

    if not isfile(json_filepath):
        raise FileNotFoundError('The file {} isn\'t found or isn\'t an absolute path.')

    # Open .json
    with open(json_filepath) as f:
        library = load(f)

    processed_tasks = dict()

    # Load library path
    if 'library_path' in library:  # Use specified library path
        library_path = library['library_path']

        # Make sure the library path ends with '/'
        if library_path.endswith('/'):
            library_path = library_path[:-1]
            # print('\tRemoved the last \'/\' from library_path, which is now: {}.'.format(library_path))

        # # Make sure the library path does not end with '/'
        # if not library_path.endswith('/'):
        #     library_path += '/'
        #     if verbose:
        #         print('\tAppended \'/\' to library_path, which is now: {}.'.format(library_path))

        if not isdir(library_path):  # Use absolute path
            library_path = join(HOME_DIR, library_path)
            # print('\tConverted the library path to the absolute path relative to the $HOME directory: {}.'.format(
            #     library_path))

    else:  # Guess library path to be found in the same direcotry as this .json
        library_path = join(split(json_filepath)[0], '')
        # print('\tNo library path is specified for {} library so guessed to be {}.'.format(library_name, library_path))

    # Load library name
    library_name = library['library_name']

    # Load library tasks
    tasks = library['tasks']
    for t in tasks:

        # Task label is this task's UID; so no duplicates are allowed
        label = t['label']
        if label in processed_tasks:
            raise ValueError('Multiple \'{}\' task labels found; use unique task label for each task.'.format(label))
        else:
            processed_tasks[label] = dict()

        processed_tasks[label]['library_path'] = library_path
        processed_tasks[label]['library_name'] = library_name

        # Load task function name
        processed_tasks[label]['function_name'] = t['function_name']

        if 'description' in t:  # Load task escription
            processed_tasks[label]['description'] = t['description']
        else:
            processed_tasks[label]['description'] = ''

        # Load task required, optional, and/or default arrguments
        for arg_type in ['required_args', 'optional_args', 'default_args']:
            if arg_type in t:
                processed_tasks[label][arg_type] = process_args(t[arg_type])
            else:
                processed_tasks[label][arg_type] = []

        # Load task returns
        if 'returns' in t:
            processed_tasks[label]['returns'] = process_returns(t['returns'])
        else:
            processed_tasks[label]['returns'] = []

    return processed_tasks


def process_args(dicts):
    """

    :param dicts: list; list of dict
    :return: dict;
    """

    processed_dicts = []

    for d in dicts:
        processed_d = dict()

        # Load arg_name
        processed_d['arg_name'] = d['arg_name']

        if 'value' in d:  # Load default value
            processed_d['value'] = d['value']
        else:
            processed_d['value'] = ''

        if 'label' in d:  # Load label
            processed_d['label'] = d['label']
        else:  # Set label as the arg_name
            processed_d['label'] = title_str(d['arg_name'])

        if 'description' in d:  # Load description
            processed_d['description'] = d['description']
        else:
            processed_d['description'] = 'No description :('

        processed_dicts.append(processed_d)

    return processed_dicts


def process_returns(dicts):
    """

    :param dicts: list; list of dict
    :return: dict;
    """

    processed_dicts = []

    for d in dicts:
        processed_d = dict()

        # Load label
        processed_d['label'] = d['label']

        if 'description' in d:  # Load description
            processed_d['description'] = d['description']
        else:
            processed_d['description'] = 'No description :('

        processed_dicts.append(processed_d)

    return processed_dicts


# ======================================================================================================================
# General support functions
# ======================================================================================================================
def get_name(obj, namesapce):
    """

    :param obj: object;
    :param namesapce: dict;
    :return: str;
    """

    # TODO: print non-strings as non-strings

    for obj_name_in_namespace, obj_in_namespace in namesapce.items():
        if obj_in_namespace is obj:  # obj is a existing obj
            return obj_name_in_namespace

    # obj is a str
    return '\'{}\''.format(obj)


def list_only_dirs(directory_path):
    """

    :param directory_path: str; directory with all libraries
    :return: list; sorted list of directories in directory_path
    """

    dirs = []
    for f in listdir(directory_path):
        fp = join(directory_path, f)
        if isdir(fp):
            dirs.append(fp)
    dirs = sorted(dirs)

    return dirs


def title_str(a_str):
    """
    Title a a_str.
    :param a_str: str;
    :return: str;
    """

    # Remember indices of original uppercase letters
    uppers = []
    start = end = None
    is_upper = False
    for i, c in enumerate(a_str):
        if c.isupper():
            # print('{} is UPPER.'.format(c))
            if is_upper:
                end += 1
            else:
                is_upper = True
                start = i
                end = start + 1
                # print('Start is {}.'.format(i))
        else:
            if is_upper:
                is_upper = False
                uppers.append((start, end))
                start = None
                end = start
    else:
        if start:
            uppers.append((start, end))

    # Title
    a_str = a_str.title().replace('_', ' ')

    # Upper all original uppercase letters
    for start, end in uppers:
        a_str = a_str[:start] + a_str[start: end].upper() + a_str[end:]

    # Lower some words
    for lowercase in ['a', 'an', 'the', 'and', 'but', 'or', 'for', 'nor', 'on', 'at', 'to', 'from', 'of', 'vs', 'vs']:
        a_str = a_str.replace(' ' + lowercase.title() + ' ', ' ' + lowercase + ' ')

    return a_str


def cast_string_to_int_float_bool_or_str(a_str):
    """
    Convert a_str into the following data types (return the first successful): int, float, bool, or str.
    :param a_str: str;
    :return: int, float, bool, or str;
    """

    value = a_str.strip()

    # try to cast to int or float
    for var_type in [int, float]:
        try:
            converted_var = var_type(value)
            return converted_var
        except ValueError:
            pass

    # try to cast as boolean
    if value == 'True':
        return True
    elif value == 'False':
        return False

    # return as string last priority
    return str(value)


def merge_dicts(*dicts):
    """
    Shallow copy and merge dicts into a new dict; precedence goes to
    key value pairs in latter dict.
    :param dicts: iterable of dict;
    :return: dict;
    """

    merged = dict()
    for d in dicts:
        merged.update(d)

    return merged
