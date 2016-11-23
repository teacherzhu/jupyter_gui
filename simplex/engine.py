import sys


def simplex(global_n, path_to_include, library_name, function_name,
            default_args, req_args, opt_args, return_names):
    """
    Executes named function from specified python package path.

    Takes in arguments for the named function, automatically detecting and
    casting to the appropriate data type. Returns the results of the function.

    Parameters
    ----------
    path_to_include : str
    library_name : str
    function_name : str
    req_args : dict
    opt_args : dict
    return_names : list

    Returns
    ----------
    results
        Raw output of the named function.

    """

    simplex_globals = global_n

    # Import function
    sys.path.insert(0, path_to_include)
    print('From {} importing {} ...'.format(path_to_include, function_name))
    exec('from {} import {} as function'.format(library_name, function_name))

    # Process args
    args = process_args(default_args, req_args, opt_args, simplex_globals)

    # Execute
    return locals()['function'](**args)


def process_args(default_args, req_args, opt_args, simplex_globals):
    """

    :param req_args: dictionary;
    :param opt_args: dictionary;
    :return: dictionary;
    """

    args = merge_dicts(default_args, req_args, opt_args)
    processed_args = {}

    for k, v in args.items():
        print('arg-key: {}; arg-val: {}'.format(k, v))

        # process as variable from notebook environment
        if v in simplex_globals:
            processed = simplex_globals[v]
            print('+ {} in globals()'.format(v))
        # process as float/int/bool/string
        else:
            processed = [cast_string_to_int_float_bool_or_str(
                s) for s in v.split(',') if s]
            print('- {} converted to {}'.format(v, type(processed[0])))

            if len(processed) == 1:
                processed = processed[0]

        processed_args[k] = processed
    return processed_args


def merge_dicts(*dicts):
    """
    Shallow copy and merge dicts into a new dict; precedence goes to
    key value pairs in latter dict.
    :param dicts: iterable of dict;
    :return: dict;
    """

    merged = {}
    for d in dicts:
        merged.update(d)

    return merged


def cast_string_to_int_float_bool_or_str(string):
    """
    Convert string into the following data types (return the first successful):
    int, float, bool, or str.
    :param string: str;
    :return: int, float, bool, or str;
    """

    value = string.strip()

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
