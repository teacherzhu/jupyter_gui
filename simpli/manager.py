"""
Defines Manager class which:
    1) syncs the globals between Notebook and Simpli;
    2) keeps track of tasks, which can be added from JSON or Notebook cell;
    3) provides access to tasks;
    4) converts task widgets into code cells; and
    5) executes task widget.
"""

import ast
# Don't remove importing sys and inspect: they are used within eval()
import sys
from inspect import _empty, signature
from json import dumps, loads
from os import listdir
from os.path import join

from . import SIMPLI_JSON_DIR
from .support import (cast_str_to_int_float_bool_or_str, get_name,
                      remove_nested_quotes, reset_encoding)


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

        # Register tasks from JSONs
        self._update_tasks_from_jsons()

    def _print(self, str_):
        """
        Print str_.
        :param str_: str; message to printed
        :return: None
        """

        if self._verbose:
            print(str_)

    def update_globals(self, globals_):
        """
        globals_ ==> self._globals & self._globals ==> globals()
        :return: None
        """

        self._globals.update(globals_)
        globals().update(self._globals)

    def _update_tasks(self, tasks):
        """
        Set or update self._tasks with tasks.
        :param tasks: dict;
        :return: None
        """

        self._print('Updating tasks {} with {} ...'.format(self._tasks, tasks))

        self._tasks.update(tasks)

    def get_tasks(self, update_tasks_from_jsons=True, print_return=True):
        """
        Get all tasks.
        :param update_tasks_from_jsons: bool;
        :param print_return: bool;
        :return: None
        """

        if update_tasks_from_jsons:
            self._update_tasks_from_jsons()

        if print_return:  # For communicating with JavaScript
            print(dumps(self._tasks))
        return self._tasks

    def get_task(self,
                 task_label=None,
                 notebook_cell_text=None,
                 print_return=True):
        """
        Get an existing task by querying for its ID; or register a task from a
        notebook cell.
        :param task_label: str;
        :param notebook_cell_text: str;
        :param print_return: bool;
        :return: dict;
        """

        self._print('Getting task {} ...'.format(task_label))

        if task_label:
            task = {task_label: self._tasks[task_label]}

        elif notebook_cell_text:
            task = self._load_task_from_notebook_cell(notebook_cell_text)

        else:
            raise ValueError(
                'Get an existing task by querying for its ID or register a '
                'task from a notebook cell.')

        if print_return:  # For communicating with JavaScript
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

                self._print('\tLoaded {}: {}.'.format(label, tasks[label]))

            self._update_tasks(tasks)
            return tasks

    def _process_args(self, args):
        """
        Process args.
        :param args: list; list of arg dict
        :return: dict;
        """

        processed_dicts = []

        for d in args:
            processed_dicts.append({
                'name':
                d.get('name'),
                'value':
                d.get('value', ''),
                'label':
                d.get('label', 'Label for {}'.format(d.get('name'))),
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
        self._print('lines: {}\n'.format(lines))

        # Get comment lines and get label (line 1) and description (line 1<)
        comment_lines = [l.strip() for l in lines if l.startswith('#')]
        self._print('comment_lines: {}\n'.format(comment_lines))
        label = ''.join(comment_lines[0].replace('#', '')).strip()
        self._print('label: {}\n'.format(label))
        description = '\n'.join(
            [l.replace('#', '').strip() for l in comment_lines[1:]])
        self._print('description: {}\n'.format(description))

        # Make AST and get returns
        m = ast.parse(text)
        b = m.body[-1]
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
                    'label': 'Label for {}'.format(t.id),
                    'description': '',
                    'value': t.id,
                })
        elif not isinstance(b, ast.Expr):
            raise ValueError('Not ast.Assign or ast.Expr.')
        self._print('returns: {}\n'.format(returns))

        # Get code lines
        code_lines = []
        for l in lines:
            if l.startswith('#'):
                continue
            else:
                l = l.strip()
                if l.startswith('sys.path.insert(') or l.startswith('import '):
                    exec(l)
                else:
                    code_lines.append(l)

        self._print(
            'code_lines (processed path & import): {}\n'.format(code_lines))

        # Get function name
        l = code_lines[0]
        if returns:
            function_name = l[l.find('=') + 1:l.find('(')].strip()
        else:
            function_name = l[:l.find('(')].strip()
        self._print('function_name: {}\n'.format(function_name))

        # Get args and kwargs
        args = []
        kwargs = []
        for al in [
                l for l in code_lines
                if not (l.endswith('(') or l.startswith(')'))
        ]:

            if '#' in al:  # Has description
                al, d = al.split('#')
                al = al.strip()
                d = d.strip()
            else:
                d = ''

            if al.endswith(',') or al.endswith(')'):
                al = al[:-1]

            if '=' in al:  # Is kwarg
                n, v = al.split('=')
                kwargs.append((n, v, d))

            else:  # Is arg
                args.append((al, d))
        self._print('args: {}\n'.format(args))
        self._print('kwargs: {}\n'.format(kwargs))

        # Get function's signature
        self._print('inspecting parameters ...')
        s = eval('signature({})'.format(function_name))
        for k, v in s.parameters.items():
            self._print('\t{}: {}'.format(k, v))

        # Get required args
        required_args = [{
            'label': 'Label for {}'.format(n),
            'description': d,
            'name': n,
            'value': v,
        } for n, (v, d) in zip(
            [v.name for v in s.parameters.values()
             if v.default == _empty], args)]
        self._print('required_args: {}\n'.format(required_args))

        # Get optional args
        optional_args = [{
            'label': 'Label for {}'.format(n),
            'description': d,
            'name': n,
            'value': v,
        } for n, v, d in kwargs]
        self._print('optional_args: {}\n'.format(optional_args))

        # Get module name
        module_name = eval('{}.__module__'.format(function_name))
        self._print('module_name: {}\n'.format(module_name))

        # Get module path
        if module_name == '__main__':  # Function is defined within this
            # Notebook
            module_path = ''
        else:  # Function is imported from a module
            module_path = eval('{}.__globals__.get(\'__file__\')'.format(
                function_name)).split(module_name.replace('.', '/'))[0]
        self._print('module_path: {}\n'.format(module_path))

        # Make a task
        task = {
            label: {
                'description': description,
                'library_path': module_path,
                'library_name': module_name,
                'function_name': function_name.split('.')[-1],
                'required_args': required_args,
                'default_args': [],
                'optional_args': optional_args,
                'returns': returns,
            }
        }
        self._print('task: {}\n'.format(task))

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

        # TODO: remove (for communicating with JavaScript)
        if isinstance(task, str):  # task is a JSON str
            # Read JSON str as dict
            task = loads(task)

        self._print('Representing task {} as code ...\n'.format(task))

        label, info = list(task.items())[0]

        description = info.get('description')
        self._print('description: {}'.format(description))

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

        # Write code
        code = '# {}\n'.format(label)

        if description:
            code += '# {}\n'.format(description)

        if function_name not in self._globals:  # Import root module
            if library_name not in self._globals:
                if library_path:
                    code += 'import sys\n'
                    code += 'sys.path.insert(0, \'{}\')\n'.format(library_path)
                code += 'import {}\n'.format(library_name.split('.')[0])

        # Style library name
        if library_name:
            library_name += '.'

        # Style returns
        returns = ', '.join([d.get('value', '') for d in returns])
        if returns:
            returns += ' = '

        # Style args
        sargs = ''
        for a in required_args:
            sargs += '\n    '
            sargs += '{}  # {},'.format(a.get('value'),
                                       a.get('description')).strip()
        for a in optional_args:
            sargs += '\n    '
            sargs += '{}={}  # {},'.format(
                a.get('name'), a.get('value'), a.get('description')).strip()
        sargs += '\n'

        # Add function code
        code += '{}{}{}({})'.format(returns, library_name, function_name,
                                    sargs)

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

        # TODO: remove (for communicating with JavaScript)
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
        returned = self._path_import_execute(info['library_path'],
                                             info['library_name'],
                                             info['function_name'], args)

        # Get returns
        returns = [r['value'] for r in info['returns']]
        self._print('returns: {}'.format(returns))

        # Handle returns
        if len(returns) == 1:
            self._globals[returns[0]] = remove_nested_quotes(returned)

        elif len(returns) > 1:
            for n, v in zip(returns, returned):
                self._globals[n] = remove_nested_quotes(v)

        self._print('self._globals after execution: {}.'.format(self._globals))

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

        merged_args = {}
        merged_args.update(required_args)
        merged_args.update(default_args)
        merged_args.update(optional_args)

        processed_args = {}
        for n, v in merged_args.items():

            if v in self._globals:  # Process as already defined variable from
                #  the Notebook environment
                processed_v = self._globals[v]

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
                n, v, get_name(processed_v, self._globals), type(processed_v)))

        return processed_args

    def _path_import_execute(self, library_path, library_name, function_name,
                             args):
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
                n, get_name(v, self._globals), type(v)))

        return locals()[function_name](**args)
