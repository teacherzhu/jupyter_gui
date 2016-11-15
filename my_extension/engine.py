import sys


def simplex(path_to_include, library_name, function_name, req_args, opt_args, return_names):
    """

    :param path_to_include:
    :param library_name:
    :param function_name:
    :param req_args:
    :param opt_args:
    :param return_names:
    :return:
    """

    # Import function
    sys.path.insert(0, path_to_include)
    print('Importing {} ...'.format(function_name))
    exec('from {} import {} as function'.format(library_name, function_name))

    # Process args
    args = process_args(req_args, opt_args)

    # Execute
    returned = locals()['function'](**args)

    for n, r in zip(return_names, returned):
        exec('globals()["{}"] = {}'.format(n, r))


def process_args(req_args, opt_args):
    """

    :param req_args: dicitonary;
    :param opt_args: dicitonary;
    :return: dictionary;
    """

    args = merge_dicts(req_args, opt_args)
    processed_args = {}

    names = globals()
    for n, arg in args.items():
        if arg in names:  # Use defined name
            a = names[arg]
            print('Argument: \'{}\' ==> {} ...'.format(arg, a))
        else:
            if ',' in arg:  # Assume iterable
                arg = arg.split(',')
                arg = [cast_string_to_int_float_bool_or_str(s) for s in arg]
                print('Argument: \'{}\' ==> {} ...'.format(arg, a))
            a = arg

        processed_args[n] = a

    return processed_args


def process_kwargs(kwargs):
    """

    :param kwargs: dict;
    :return: dict;
    """

    processed_kwargs = kwargs

    return processed_kwargs


def merge_dicts(*dicts):
    """
    Shallow copy and merge dicts into a new dict; precedence goes to key value pairs in latter dict.
    :param dicts: iterable of dict;
    :return: dict;
    """

    merged = {}
    for d in dicts:
        merged.update(d)

    return merged


def cast_string_to_int_float_bool_or_str(string):
    """
    Convert string into the following data types (return the first successful): int, float, bool, or str.
    :param string: str;
    :return: int, float, bool, or str;
    """

    value = string.strip()

    for var_type in [int, float]:
        try:
            converted_var = var_type(value)
            return converted_var
        except ValueError:
            pass

    if value == 'True':
        return True
    elif value == 'False':
        return False

    return str(value)
