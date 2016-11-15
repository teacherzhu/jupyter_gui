import sys

"""
    # Parse returned values
    for n, r in zip(return_names, simplex(...)):
        exec('global {}'.format(n))
        exec('{} = r'.format(n))
"""


def simplex(path_to_include, library_name, function_name, args, return_names, kwargs):
    """
    """

    # Import function
    sys.path.insert(0, path_to_include)
    print('Importing {} ...'.format(function_name))
    exec('from {} import {} as function'.format(library_name, function_name))

    # Process args and kwargs
    processed_args = process_args(args)
    processed_kwargs = process_kwargs(kwargs)

    print(processed_args, processed_kwargs)
    # Execute
    returned = locals()['function'](*processed_args, **processed_kwargs)

    for n, r in zip(return_names, returned):
        exec('globals()["{}"] = {}'.format(n, r))


def process_args(args):
    """

    :param args: dicitonary;
    :return: list;
    """

    processed_args = {}

    names = globals()
    for i, arg in enumerate(args):
        if arg in names:   # Use defined name
            a = names[arg]
            print('Argument #{}: \'{}\' ==> {} ...'.format(i, arg, a))
        else:
            if ',' in arg:  # Assume iterable
                arg = arg.split(',')
                arg = [cast_string_to_int_float_bool_or_str(a) for a in arg]
                print('Argument #{}: \'{}\' ==> {} ...'.format(i, arg, a))

            a = arg

        processed_args.append(a)

    return processed_args


def process_kwargs(kwargs):
    """

    :param kwargs: dict;
    :return: dict;
    """

    processed_kwargs = kwargs

    return processed_kwargs


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
