from os import listdir
from os.path import join, isdir


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


def cast_str_to_int_float_bool_or_str(a_str):
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


def reset_encoding(a_str):
    """

    :param a_str: str;
    :return: str;
    """

    return a_str.replace(u'\u201c', '"').replace(u'\u201d', '"')


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
