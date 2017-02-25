def a_function_in_a_file(req_arg1, req_arg2, opt_arg1=None, opt_arg2=None):
    """
    A function in a library.
    :param req_arg1: object; required argument 1.
    :param req_arg2: object; required argument 2.
    :param opt_arg1: object; optional argument 1.
    :param opt_arg2: object; optional argument 2.
    :return: None
    """

    prefix = '<A function in a file>'
    print('{} Required argument 1 & 2: {} & {}.'.format(prefix, req_arg1, req_arg2))
    if opt_arg1:
        print('{} Optional argument 1: {}.'.format(prefix, opt_arg1))
    if opt_arg2:
        print('{} Optional argument 2: {}.'.format(prefix, opt_arg2))
