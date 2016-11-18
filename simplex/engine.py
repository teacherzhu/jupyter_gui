import sys


def test_setting_global_variable(returns=()):
    globals()['*** TEST 1 ***'] = '*** TEST 1 ***'
    print(globals())
    print('\n\n')

    global TEST_2
    TEST_2 = '*** TEST 2 ***'
    print(globals())
    print('\n\n')

    if any(returns):
        returns.append('*** TEST 3 ***')
        print(globals())
        print('\n\n')


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
    print('From {} importing {} ...'.format(path_to_include, function_name))
    exec('from {} import {} as function'.format(library_name, function_name))

    # Process args
    args = process_args(req_args, opt_args)

    # Execute
    returned = locals()['function'](**args)

    for n, r in zip(return_names, returned):
        globals()[n] = r
    global x
    x = 1000


def process_args(req_args, opt_args):
    """

    :param req_args: dicitonary;
    :param opt_args: dicitonary;
    :return: dictionary;
    """

    args = merge_dicts(req_args, opt_args)
    processed_args = {}

    names = globals()

    for k, v in args.items():

        if v in names:  # Use defined name
            processed = names[v]
            print('Argument: \'{}\' ==> {} ...'.format(v, processed))

        else:  # Process arguments
            if isinstance(v, int) or isinstance(v, float):
                processed = v

            elif ',' in v:  # Assume iterable
                processed = [cast_string_to_int_float_bool_or_str(s) for s in v.split(',') if s]
                print('Argument: \'{}\' ==> {} ...'.format(v, processed))

            else:  # Using as it is (str)
                processed = v

        processed_args[k] = processed

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
