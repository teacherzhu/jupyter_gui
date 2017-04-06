"""
Defines Manager class which:
    1) syncs the globals between Notebook and Simpli;
    2) keeps track of tasks, which can be added from JSON or Notebook cell;
    3) converts task widgets into code cells; and
    4) executes task widget.
"""

import ast
# Don't remove importing sys and inspect: they are used within eval()
import sys
from inspect import _empty, signature
from json import dumps, loads
from os import listdir
from os.path import isdir, join

from .default_tasks import SIMPLI_JSON_DIR
from .support import (cast_str_to_int_float_bool_or_str, get_name, merge_dicts,
                      remove_nested_quotes, reset_encoding)


# TODO: communicate with JavaScript without dumps or printing


class Manager:
    """
    Notebook Manager.
    """

    def __init__(self, verbose=False):
        """
        Initialize a Notebook Manager.
        """

        self._verbose = verbose

        # Globals
        self._globals = {}

        # Tasks (dict) keyed by their label (unique ID)
        self._tasks = {}

    def _print(self, str_):
        """
        Print str_.
        :param str_: str; message to printed
        :return: None
        """

        if self._verbose:
            print(str_)

    # ==========================================================================
    # globals property
    # ==========================================================================
    def _get_globals(self):
        """
        Get globals.
        :return: dict;
        """

        return self._globals

    def _set_globals(self, globals_):
        """
        Set globals.
        :param globals_: dict;
        :return: None
        """

        self._globals = globals_

    globals_ = property(_get_globals, _set_globals)

    def import_export_globals(self, globals_):
        """
        Import globals and export globals.
        :param globals_: dict;
        :return: None
        """

        self._print('Importing globals: {} ...'.format(globals_))
        self.globals_ = merge_dicts(self.globals_, globals_)

        self._print('Exporting globals: {} ...'.format(self.globals_))
        for n, v in self.globals_.items():
            globals()[n] = v

    # ==========================================================================
    # tasks property
    # ==========================================================================
    def _get_tasks(self):
        """
        Get tasks.
        :return: list; list of dict
        """

        return self._tasks

    def _set_tasks(self, tasks):
        """
        Set tasks.
        :param tasks: list; list of dict
        :return: None
        """

        self._tasks = tasks

    tasks = property(_get_tasks, _set_tasks)

    def print_tasks(self, update_tasks_from_jsons=True):
        """
        Print tasks to communicate with JavaScript.
        :return: None
        """

        self._print('Printing tasks in JSON str ...')

        if update_tasks_from_jsons:
            self._update_tasks_from_jsons()

        print(dumps(self._tasks))

    def _update_tasks(self, tasks):
        """
        Set or update self.tasks with tasks.
        :param tasks: dict;
        :return: None
        """

        self._print('Updating tasks {} with {} ...'.format(self.tasks, tasks))

        self.tasks = merge_dicts(self.tasks, tasks)

    def get_task(self,
                 task_label=None,
                 notebook_cell_text=None,
                 print_as_json=True):
        """
        Get a task, whose label is task_label.
        :param task_label: str;
        :param notebook_cell_text: str;
        :param print_as_json: bool;
        :return: dict;
        """

        self._print('Getting task {} ...'.format(task_label))

        if task_label:
            task = {task_label: self.tasks[task_label]}

        elif notebook_cell_text:
            task = self._load_task_from_notebook_cell(notebook_cell_text)

        else:
            raise ValueError(
                'Get an existing task by querying for its ID or register a '
                'task from a notebook cell.')

        if print_as_json:
            print(dumps(task))

        return task

    # ==========================================================================
    # Get a task(s) from JSON(s)
    # ==========================================================================
    def _update_tasks_from_jsons(self):
        """
        Load tasks from a task-specifying JSON or JSONs in a directory.
        :return: dict;
        """

        tasks = {}

        for fn in listdir(SIMPLI_JSON_DIR):
            fp = join(SIMPLI_JSON_DIR, fn)

            self._print('Loading task-specifying JSON {} ...'.format(fp))

            with open(fp) as f:
                tasks_json = loads(reset_encoding(f.read()))

            # Load library path, which is common for all tasks in this JSON
            library_path = tasks_json['library_path']
            if not isdir(library_path):
                self._print('library_path doesn\'t exist.')

            # Load each task
            for t in tasks_json['tasks']:

                # Split function path into library_name and function_name
                function_path = t['function_path']
                if '.' in function_path:
                    split = function_path.split('.')
                    library_name = '.'.join(split[:-1])
                    function_name = split[-1]
                else:
                    raise ValueError(
                        'function_path must be like: \'file.function\'.')

                # Task label is this task's UID; so no duplicates are allowed
                label = t.get('label',
                              '{} (no task label)'.format(function_name))
                if label in tasks or label in self.tasks:  # Label is duplicated
                    self._print(
                        'Task label \'{}\' is duplicated; making a new task '
                        'label ...'.format(label))
                    i = 2
                    new_label = '{} (v{})'.format(label, i)
                    while new_label in tasks:
                        i += 1
                        new_label = '{} (v{})'.format(label, i)
                    label = new_label

                tasks[label] = {
                    'library_path':
                    library_path,
                    'library_name':
                    library_name,
                    'function_name':
                    function_name,
                    'description':
                    t.get('description', 'No description.'),
                    'required_args':
                    self._process_args(t.get('required_args', [])),
                    'default_args':
                    self._process_args(t.get('default_args', [])),
                    'optional_args':
                    self._process_args(t.get('optional_args', [])),
                    'returns':
                    self._process_returns(t.get('returns', [])),
                }

                self._print(
                    '\t\tLoaded task {}: {}.'.format(label, tasks[label]))

            self._update_tasks(tasks)
            return tasks

    def _process_args(self, args):
        """
        Process args.
        :param args: list; list of arg dict
        :return: dict;
        """

        self._print('Processing args ...')

        processed_dicts = []

        for d in args:
            processed_dicts.append({
                'name':
                d.get('name'),
                'value':
                d.get('value', ''),
                'label':
                d.get('label', '{} Label'.format(d.get('name'))),
                'description':
                d.get('description', 'No description.'),
            })

        return processed_dicts

    def _process_returns(self, returns):
        """
        Process returns.
        :param returns: list; list of return dict
        :return: dict;
        """

        self._print('Processing returns ...')

        processed_dicts = []

        for d in returns:
            processed_dicts.append({
                'label':
                d.get('label'),
                'description':
                d.get('description', 'No description.'),
            })

        return processed_dicts

    # ==========================================================================
    # Get a task from a Notebook cell
    # ==========================================================================
    def _load_task_from_notebook_cell(self, text):
        """
        Load a task from a noteboos cell.
        :param text: str;
        :return: dict; {str: str}
        """

        # Split text into lines
        lines = text.split('\n')
        print('lines: {}\n'.format(lines))

        # Get comment lines
        comment_lines = [l.strip() for l in lines if l.startswith('#')]
        print('comment_lines: {}\n'.format(comment_lines))

        # Get label from the 1st comment line
        label = ''.join(comment_lines[0].split('#')[1:]).strip()
        print('label: {}\n'.format(label))

        # Get code lines
        code_lines = [l.strip() for l in lines if not l.startswith('#')]
        print('comment_lines: {}\n'.format(comment_lines))

        # Make AST
        m = ast.parse(text)
        b = m.body[0]

        # Get returns
        returns = []
        if isinstance(b, ast.Assign):

            peek = b.targets[0]
            if isinstance(peek, ast.Tuple):
                targets = peek.elts
            elif isinstance(peek, ast.Name):
                targets = b.targets
            else:
                raise ValueError('Unknown target class: {}.'.format(peek))

            for t in targets:
                returns.append({
                    'label': '{} Label'.format(t.id),
                    'description': 'Description.',
                    'value': t.id,
                })
        print('returns: {}\n')

        # Get function name
        function_name = b.value.func.id
        print('function_name: {}\n'.format(function_name))

        # Get args and kwargs
        args = []
        kwargs = {}
        for a in [
                l for l in code_lines
                if not (l.endswith('(') or l.startswith(')'))
        ]:

            if '=' in a:  # kwarg
                k, v = a.split('=')
                if v.endswith(','):
                    v = v[:-1]
                kwargs[k] = v

            else:  # arg
                if a.endswith(','):
                    a = a[:-1]
                args.append(a)
        print('args: {}\n'.format(args))
        print('kwargs: {}\n'.format(kwargs))

        # Get function's signature
        print('inspecting parameters ...')
        s = eval('signature({})'.format(function_name))
        for k, v in s.parameters.items():
            print('\t{}: {}'.format(k, v))

        # Get required args
        required_args = [{
            'label': '{} Label'.format(n),
            'description': 'Description.',
            'name': n,
            'value': v,
        } for n, v in zip(
            [v.name for v in s.parameters.values()
             if v.default == _empty], args)]
        print('required_args: {}\n'.format(required_args))

        # Get optional args
        optional_args = [{
            'label': '{} Label'.format(n),
            'description': 'Description.',
            'name': n,
            'value': v,
        } for n, v in kwargs.items()]
        print('optional_args: {}\n'.format(optional_args))

        # Get module name
        module_name = eval('{}.__module__'.format(function_name))
        print('module_name: {}\n'.format(module_name))

        # Get module path
        if module_name == '__main__':  # Function is defined within this
            # Notebook
            module_path = ''
        else:  # Function is imported from a module
            module_path = eval('{}.__globals__.get(\'__file__\')'.format(
                function_name)).split(module_name.replace('.', '/'))[0]
        print('module_path: {}\n'.format(module_path))

        # Make a task
        task = {
            label: {
                'description': 'Description.',
                'library_path': module_path,
                'library_name': module_name,
                'function_name': function_name,
                'required_args': required_args,
                'default_args': [],
                'optional_args': optional_args,
                'returns': returns,
            }
        }
        print('task: {}\n'.format(task))

        # Register this task
        self._update_tasks(task)

        return task

    # ==========================================================================
    # Code task
    # ==========================================================================
    def code_task(self, task, print_return=True):
        """
        Represent task as code.
        :param task:  dict;
        :param print_return: bool;
        :return: str; code representation of task
        """

        if isinstance(task, str):  # task is a JSON str
            # Read JSON str as dict
            task = loads(task)

        self._print('Representing task ({}) as code ...\n'.format(task))

        label, info = list(task.items())[0]
        library_path = info.get('library_path')
        self._print('library_path: {}'.format(library_path))
        library_name = info.get('library_name')
        self._print('library_name: {}'.format(library_name))
        function_name = info.get('function_name')
        self._print('function_name: {}'.format(function_name))
        required_args = info.get('required_args')
        self._print('required_args: {}'.format(required_args))
        default_args = info.get('default_args')
        self._print('default_args: {}'.format(default_args))
        optional_args = info.get('optional_args')
        self._print('optional_args: {}'.format(optional_args))
        returns = info.get('returns')
        self._print('returns: {}'.format(returns))

        args_d = {}
        for a in required_args + default_args + optional_args:
            args_d[a['name']] = a['value']

        if library_path:
            exec('sys.path.insert(0, \'{}\')'.format(library_path))

        # Import function
        exec('from {} import {}'.format(library_name, function_name))

        s = eval('signature({})'.format(function_name))

        # Args
        args_l = [
            '{}={}'.format(n, self._str_or_name(args_d[n]))
            for n in s.parameters if n in args_d
        ]
        self._print('args_l (_str_or_named): {}'.format(args_l))

        # Keyword args
        kwargs_l = [
            '\'{}\':{}'.format(n, self._str_or_name(v))
            for n, v in args_d.items() if n not in s.parameters
        ]
        self._print('kwargs_l (_str_or_named): {}'.format(kwargs_l))

        # _str_or_name returns
        returns = ', '.join([d.get('value') for d in returns])
        self._print('returns (_str_or_named): {}'.format(returns))

        # Build code
        code = ''

        if library_name.startswith('simpli') and False:  # Use custom code
            # Get custom code
            custom_code = 'TODO: enable custom code for default functions'
            code += '# {}\n{}{}\n'.format(label, returns, custom_code)

        elif function_name not in self.globals_:  # Import function - fully
            code += 'import sys\nsys.path.insert(0, \'{}\')\nimport {' \
                    '}\n\n'.format(
                library_path, library_name.split('.')[0])
        else:  # A non-simpli function in globals
            library_name = ''

        # Style returns
        if returns:
            returns += ' = '

        # Style library name
        if library_name == '__main__':
            library_name = ''
        elif library_name:
            library_name += '.'

        # Make args separator
        sep = ',\n' + ' ' * (len(returns + library_name + function_name) +
                             library_name.count('.') - 1)

        if kwargs_l:
            kwargs_s = sep + '**{'
            kwargs_s += (sep + '   ').join(kwargs_l)
            kwargs_s += sep + '  }'
        else:
            kwargs_s = '{}'

        # Add function code
        code += '# {}\n{}{}{}({}{}{})'.format(label, returns, library_name,
                                              function_name,
                                              sep.join(args_l), kwargs_s, sep)

        if print_return:
            print(code)
        return code

    # ==========================================================================
    # Execute task
    # ==========================================================================
    def execute_task(self, task):
        """
        Execute a task.
        :param task: dict;
        :return: None
        """

        if isinstance(task, str):
            task = loads(task)

        label, info = list(task.items())[0]

        # Process and merge args
        required_args = {
            a['name']: remove_nested_quotes(a['value'])
            for a in info['required_args']
        }
        default_args = {
            a['name']: remove_nested_quotes(a['value'])
            for a in info['default_args']
        }
        optional_args = {
            a['name']: remove_nested_quotes(a['value'])
            for a in info['optional_args']
        }
        args = self._merge_and_process_args(required_args, default_args,
                                            optional_args)

        # Execute function
        returned = self._path_import_and_execute(info['library_path'],
                                                 info['library_name'],
                                                 info['function_name'], args)

        # Get returns
        returns = [r['value'] for r in info['returns']]
        self._print('returns: {}'.format(returns))

        # Handle returns
        if len(returns) == 1:
            self.globals_[returns[0]] = remove_nested_quotes(returned)

        elif len(returns) > 1:
            for n, v in zip(returns, returned):
                self.globals_[n] = remove_nested_quotes(v)

        self._print('self.globals_ after execution: {}.'.format(self.globals_))

    def _merge_and_process_args(self, required_args, default_args,
                                optional_args):
        """
        Convert input str arguments to corresponding values:
            If the str is the name of a existing variable in the Notebook
            globals, use its corresponding value;
            If the str contains ',', convert it into a list of str;
            Try to cast str in the following order and use the 1st match:
            int, float, bool, and str;
        :param required_args: dict;
        :param default_args: dict;
        :param optional_args: dict;
        :return: dict; merged and processed args
        """

        self._print('\tMerging and processing arguments ...')

        if None in required_args or '' in required_args:
            raise ValueError('Missing required_args.')

        repeating_args = set(required_args.keys() & default_args.keys() &
                             optional_args.keys())
        if any(repeating_args):
            raise ValueError(
                'Argument \'{}\' is repeated.'.format(required_args))

        merged_args = merge_dicts(required_args, default_args, optional_args)

        processed_args = {}
        for n, v in merged_args.items():

            if v in self.globals_:  # Process as already defined variable from
                #  the Notebook environment
                processed_v = self.globals_[v]

            else:  # Process as float, int, bool, or str
                # First assume a list of str to be passed
                processed_v = [
                    cast_str_to_int_float_bool_or_str(s) for s in v.split(',')
                    if s
                ]

                if len(processed_v
                       ) == 1:  # If there is only 1 item in the assumed list,
                    # use it directly
                    processed_v = processed_v[0]

            processed_args[n] = processed_v
            self._print('\t\t{}: {} > {} ({})'.format(
                n, v, get_name(processed_v, self.globals_), type(processed_v)))

        return processed_args

    def _path_import_and_execute(self, library_path, library_name,
                                 function_name, args):
        """
        Prepend path, import library, and execute task.
        :param library_path: str;
        :param library_name: str;
        :param function_name: str;
        :param args: dict;
        :return: list; raw output of the function
        """

        self._print(
            'Updating path, importing function, and executing task ...')

        # Prepend library path
        if library_path:
            code = 'sys.path.insert(0, \'{}\')'.format(library_path)
            self._print('\t{}'.format(code))
            exec(code)

        # Import function
        code = 'from {} import {}'.format(library_name, function_name)
        self._print('\t{}'.format(code))
        exec(code)

        # Execute
        self._print('\tExecuting {} with:'.format(locals()[function_name]))
        for n, v in sorted(args.items()):
            self._print('\t\t{} = {} ({})'.format(
                n, get_name(v, self.globals_), type(v)))

        return locals()[function_name](**args)

    # TODO: consider removing
    # ==========================================================================
    # Support function
    # ==========================================================================
    def _str_or_name(self, str_):
        """
        If str_ is an existing name in the current globals, then return str_.
        Else if str_ is a str, then return 'str_'.
        :param str_: str;
        :return: str;
        """

        str_ = remove_nested_quotes(str_)

        if str_ in self.globals_ or not isinstance(
                cast_str_to_int_float_bool_or_str(str_), str):  # object
            return str_
        else:  # str
            return '\'{}\''.format(str_)
