"""
Defines Manager class which:
    1) syncs the namespace between Notebook and Simpli;
    2) keeps track of tasks, which can be added from JSON or Notebook cell;
    3) makes code representation of task widgets (during task widget ==(flip)==> code);
    4) executes function;
    5) ;
"""

import sys  # Don't remove this import - sys IS used!
from os import listdir
from os.path import isdir, join
import inspect  # Don't remove this import - inspect IS used!
from json import loads, dumps

from IPython.display import clear_output

from . import HOME_DIR, SIMPLI_JSON_DIR
from .support import get_name, merge_dicts, remove_nested_quotes, title_str, cast_str_to_int_float_bool_or_str, \
    reset_encoding


class Manager:
    """
    Notebook Manager.
    """

    def __init__(self, verbose=False):
        """
        Initialize a Notebook Manager.
        """

        self._namespace = {}

        # Tasks (and their specifications) keyed by their unique label
        self._tasks = {}

        self._verbose = verbose

    def _print(self, str_):
        """
        Print str_.
        :param str_: str; message to printed
        :return: None
        """

        if self._verbose:
            print(str_)

    def _get_namespace(self):
        """
        Get namespace.
        :return: dict;
        """

        # self._print('(Getting namespace ...)')

        return self._namespace

    def _set_namespace(self, namespace):
        """
        Set namespace
        :param namespace: dict;
        :return: None
        """

        self._print('(Setting namespace ...)')

        self._namespace = namespace
        globals()

    namespace = property(_get_namespace, _set_namespace)

    def update_namespace(self, namespace):
        """
        Update with namespace.
        :param namespace: dict;
        :return: None
        """

        # self._print('Updating namespace with {} ...'.format(namespace))

        self.namespace = merge_dicts(self.namespace, namespace)

        for n, v in self.namespace.items():
            globals()[n] = v

    def _get_tasks(self):
        """
        Get tasks.
        :return: list; list of dict
        """

        self._print('(Getting tasks ...)')

        return self._tasks

    def _set_tasks(self, tasks):
        """
        Set tasks.
        :param tasks: list; list of dict
        :return:  None
        """

        self._print('(Setting tasks ...)')

        self._tasks = tasks

    tasks = property(_get_tasks, _set_tasks)

    def print_tasks_as_json(self, json_directory_path=SIMPLI_JSON_DIR):
        """
        Load tasks from task-specifying JSONs in json_directory_path and print all tasks in JSON format.
        :return: None
        """

        self._print('Printing tasks in JSON format ...')

        self._load_tasks_from_json_dir(json_directory_path=json_directory_path)

        print(dumps(self._tasks))

    def get_task(self, task_label=None, notebook_cell_text=None, print_as_json=True):
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
            raise ValueError('Need either task_label or notebook_cell_text.')

        if print_as_json:
            print(dumps(task))
        return task

    def _update_tasks(self, tasks):
        """
        Set or update a task, whose label is task_label, to be task.
        :param tasks: dict;
        :return: None
        """

        self._print('Setting/updating task {} to be {} ...'.format(self.tasks, tasks))

        # TODO: add only new information
        self.tasks = merge_dicts(self.tasks, tasks)

    def _load_tasks_from_json_dir(self, json_directory_path):
        """
        Load tasks from task-specifying JSONs in json_directory_path.
        :param json_directory_path: str; directory containing task-specifying JSONs
        :return: None
        """

        self._print('Loading task-specifying JSONs in directory {} ...'.format(json_directory_path))

        for f in listdir(json_directory_path):
            fp_json = join(json_directory_path, f)
            try:
                self._load_tasks_from_json(fp_json)

            except FileNotFoundError as e:
                print('FileNotFoundError (JSON doesn\'t exist or the link is broken if it\'s a link): {}'.format(e))
            except KeyError as e:
                print('JSON key error: {}'.format(e))
            except ValueError as e:
                print('ValueError: {}'.format(e))

    def _load_tasks_from_json(self, json_filepath):
        """
        Load a task from a task-specifying JSON, json_filepath
        :param json_filepath: str; filepath to a task-specifying JSON
        :return: None
        """

        self._print('Loading task-specifying JSON {} ...'.format(json_filepath))

        with open(json_filepath) as f:
            tasks_json = loads(reset_encoding(f.read()))

        tasks = {}

        # Load library path, which is common for all tasks
        library_path = tasks_json['library_path']
        if library_path and not isdir(library_path):  # Use absolute path assuming its in user-home directory
            library_path = join(HOME_DIR, library_path)
            self._print('\tAssumed that library_path ({}) is relative to the user-home directory.'.format(library_path))

        # Load each task
        for t in tasks_json['tasks']:

            # Split function path into library_name and function_name
            function_path = t['function_path']
            if '.' in function_path:
                split = function_path.split('.')
                library_name = '.'.join(split[:-1])
                function_name = split[-1]
            else:
                raise ValueError('function_path must be like: \'path.to.file.function_name\'.')

            # Task label is this task's UID; so no duplicates are allowed
            label = t.get('label', '{} (no task label)'.format(function_name))
            if label in tasks:  # Label is duplicated
                self._print('Task label \'{}\' is duplicated; automatically making a new task label ...'.format(label))

                i = 2
                new_label = '{} (v{})'.format(label, i)
                while new_label in tasks:
                    i += 1
                    new_label = '{} (v{})'.format(label, i)
                label = new_label

            tasks[label] = {
                'library_path': library_path,
                'library_name': library_name,
                'function_name': function_name,
                'description': t.get('description', 'No description.'),
                'required_args': self._process_args(t.get('required_args', [])),
                'default_args': self._process_args(t.get('default_args', [])),
                'optional_args': self._process_args(t.get('optional_args', [])),
                'returns': self._process_returns(t.get('returns', []))}

            self._print('\t\tLoaded task {}: {}.'.format(label, tasks[label]))

        self._update_tasks(tasks)

    def _load_task_from_notebook_cell(self, text):
        """
        Load task from a notebook cell.
        :param text: str;
        :return: dict;
        """

        self._print('Loading a task from a notebook cell ...')

        self._print('*********\n{}\n*********'.format(text))

        lines = [s.strip() for s in text.split('\n') if s != '']
        self._print('*** lines: {}'.format(lines))

        # Comment lines
        comment_lines = [l for l in lines if l.startswith('#')]
        self._print('*** comment lines: {}'.format(comment_lines))

        label = comment_lines[0].split('#')[1].strip()
        self._print('*** label: {}'.format(label))

        # Code lines
        code_lines = []
        for l in lines:
            if not l.startswith('#'):
                if 'path.insert' in l or 'import ' in l:  # Importing a module
                    exec(l)
                else:
                    code_lines.append(l)
        self._print('*** code lines: {}'.format(code_lines))
        code = ''.join(code_lines).replace(' ', '')

        # Get before the 1st '(' and args (after the 1st '(' without the last ')')
        i = code.find('(')
        before, args = code[:i], code[i + 1:-1]
        self._print('*** before the 1st \'(\': {}'.format(before))
        self._print('*** args (after the 1st \'(\' without the last \')\'): {}'.format(args))
        args = args.split(',')
        self._print('*** args (split): {}'.format(args))

        # Get returns
        i = before.find('=')
        if i == -1:  # '=' not found; so there is not return
            i = 0
        returns = before[:i].split(',')
        self._print('*** returns: {}'.format(returns))
        returns = [x for x in returns if x != '']
        returns = [{
                       'label': 'TODO: get from docstring',
                       'description': 'TODO: get from docstring',
                       'value': v,
                   }
                   for v in returns]

        # Get function name
        if i != 0:  # There was a '='
            # Increment index to skip '='
            i += 1
        function_name = before[i:]
        self._print('*** function_name: {}'.format(function_name))

        # Get signature
        signature = eval('inspect.signature({})'.format(function_name))
        self._print('*** signature.parameters: {}'.format(signature.parameters))

        # Get required args
        required_args = [{
                             'label': n,
                             'description': 'TODO: get from docstring',
                             'name': n,
                             'value': v,
                         }
                         for n, v in zip(list(signature.parameters), [x for x in args if '=' not in x])]
        self._print('*** required_args: {}'.format(required_args))

        # Get optional args
        optional_args = [{
                             'label': n,
                             'description': 'TODO: get from docstring',
                             'name': n,
                             'value': v,
                         }
                         for n, v in [x.split('=') for x in args if '=' in x]]
        self._print('*** optional_args: {}'.format(optional_args))

        # Get module name
        library_name = eval('{}.__module__'.format(function_name))
        self._print('*** library_name: {}'.format(library_name))

        # Get library path
        if library_name == '__main__':  # Function is defined within this Notebook
            library_path = ''
        else:  # Function is not defined within this Notebook (it's imported from a module)
            library_path = \
                eval('{}.__globals__.get(\'__file__\')'.format(function_name)).split(library_name.replace('.', '/'))[0]
            function_name = function_name.split('.')[-1]
            self._print('*** function_name (not defined within this Notebook): {}'.format(function_name))
        self._print('*** library_path: {}'.format(library_path))

        # Make a task
        task = {
            label: {
                'description': 'TODO: get from docstring',
                'library_path': library_path,
                'library_name': library_name,
                'function_name': function_name,
                'required_args': required_args,
                'default_args': [],
                'optional_args': optional_args,
                'returns': returns}
        }

        # Register this task
        self._update_tasks(task)

        return task

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
                'name': d.get('name'),
                'value': d.get('value', ''),
                'label': d.get('label', title_str(d['name'])),
                'description': d.get('description', 'No description.')}
            )

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
                'label': d.get('label'),
                'description': d.get('description', 'No description.')}
            )

        return processed_dicts

    def execute_task(self, task):
        """
        Execute task.
        :param task: dict;
        :return: None
        """

        # TODO: clear the previous output somewhere else
        # Clear any existing output
        clear_output()

        if isinstance(task, str):
            task = loads(task)

        label, info = list(task.items())[0]

        # Process and merge args
        required_args = {a['name']: remove_nested_quotes(a['value']) for a in info['required_args']}
        default_args = {a['name']: remove_nested_quotes(a['value']) for a in info['default_args']}
        optional_args = {a['name']: remove_nested_quotes(a['value']) for a in info['optional_args']}
        args = self._merge_process_args(required_args, default_args, optional_args)

        # Get returns
        returns = [a['value'] for a in info['returns']]
        if None in returns or '' in returns:
            raise ValueError('Missing returns.')
        else:
            self._print('returns: {}'.format(returns))

        # Call function
        returned = self._path_import_execute(info['library_path'], info['library_name'], info['function_name'], args)

        # Handle returns
        if len(returns) == 1:
            self.namespace[returns[0]] = remove_nested_quotes(returned)

        elif len(returns) > 1:
            for n, v in zip(returns, returned):
                self.namespace[n] = remove_nested_quotes(v)
        else:
            # TODO: think about how to better handle no-returns
            pass

        self._print('self.namespace after execution: {}'.format(self.namespace))

    def _path_import_execute(self, library_path, library_name, function_name, args):
        """
        Prepend path, import library, and execute task.
        :param library_path: str;
        :param library_name: str;
        :param function_name: str;
        :param args: dict;
        :return: list; raw output of the function
        """

        self._print('Updating path, importing function, and executing task ...')

        # Prepend library path
        if library_path:
            code = 'sys.path.insert(0, \'{}\')'.format(library_path)
            self._print('\t{}'.format(code))
            exec(code)

        # Import function
        code = 'from {} import {} as function'.format(library_name, function_name)
        self._print('\t{}'.format(code))
        exec(code)

        # Execute
        self._print('\tExecuting {} with:'.format(locals()['function']))
        for n, v in sorted(args.items()):
            self._print('\t\t{} = {} ({})'.format(n, get_name(v, self.namespace), type(v)))

        return locals()['function'](**args)

    def _merge_process_args(self, required_args, default_args, optional_args):
        """
        Convert input str arguments to corresponding values:
            If the str is the name of a existing variable in the Notebook namespace, use its corresponding value;
            If the str contains ',', convert it into a list of str;
            Try to cast str in the following order and use the 1st match: int, float, bool, and str;
        :param required_args: dict;
        :param default_args: dict;
        :param optional_args: dict;
        :return: dict; merged and processed args
        """

        self._print('\tMerging and processing arguments ...')

        if None in required_args or '' in required_args:
            raise ValueError('Missing required_args.')

        repeating_args = set(required_args.keys() & default_args.keys() & optional_args.keys())
        if any(repeating_args):
            raise ValueError('Argument \'{}\' is repeated.'.format(required_args))

        merged_args = merge_dicts(required_args, default_args, optional_args)

        processed_args = {}
        for n, v in merged_args.items():

            if v in self.namespace:  # Process as already defined variable from the Notebook environment
                processed_v = self.namespace[v]

            else:  # Process as float, int, bool, or str
                # First assume a list of str to be passed
                processed_v = [cast_str_to_int_float_bool_or_str(s) for s in v.split(',') if s]

                if len(processed_v) == 1:  # If there is only 1 item in the assumed list, use it directly
                    processed_v = processed_v[0]

            processed_args[n] = processed_v
            self._print('\t\t{}: {} > {} ({})'.format(n, v, get_name(processed_v, self.namespace), type(processed_v)))

        return processed_args

    def task_to_code(self, task, print_return=True):
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
        optional_args = info.get('optional_args')
        self._print('optional_args: {}'.format(optional_args))
        returns = info.get('returns')
        self._print('returns: {}'.format(returns))

        # _str_or_name required args
        required_args = ', '.join([self._str_or_name(d.get('value')) for d in required_args])
        self._print('required_args (_str_or_named): {}'.format(required_args))

        # _str_or_name optional args
        optional_args = ', '.join(
            ['{}={} (_str_or_named)'.format(d.get('name'), self._str_or_name(d.get('value'))) for d in optional_args])
        self._print('optional_args (_str_or_named): {}'.format(required_args))

        # _str_or_name returns
        returns = ', '.join([self._str_or_name(d.get('value')) for d in returns])
        self._print('returns (_str_or_named): {}'.format(returns))

        # Build code
        code = ''

        # TODO: enable custom code for simpli's default functions
        if library_name.startswith('simpli') and False:  # Use custom code
            # Get custom code
            exec('from {} import {}'.format(library_name, function_name))
            custom_code = eval('{}({}, {}, namespace=self.namespace)'.format(function_name,
                                                                             required_args,
                                                                             optional_args))
            code += '# {}\n{}{}\n'.format(label,
                                          returns,
                                          custom_code)

        elif function_name not in self.namespace:  # Import function - fully
            code += 'import sys\nsys.path.insert(0, \'{}\')\nimport {}\n\n'.format(library_path,
                                                                                   library_name.split('.')[0])
        else:  # A non-simpli function in namespace
            library_name = ''

        # Style returns
        if returns:
            returns += ' = '

        # Style library name
        if library_name == '__main__':
            library_name = ''
        elif library_name:
            library_name += '.'

        # Style args
        s = len(returns + library_name + function_name)
        sep = ',\n' + ' ' * s

        # Style required args
        if required_args:
            required_args = sep.join([a for a in required_args.split(',')])

        # Style optional args
        if optional_args:
            optional_args = sep.join([a for a in optional_args.split(',')])
            optional_args = sep + optional_args

        code += '# {}\n{}{}{}({}{})'.format(label,
                                            returns,
                                            library_name,
                                            function_name,
                                            required_args,
                                            optional_args)

        if print_return:
            print(code)
        return code

    def _str_or_name(self, str_):
        """
        If str_ is an existing name in the current namespace, then return str_.
        Else if str_ is a str, then return 'str_'.
        :param str_: str;
        :return: str;
        """

        str_ = remove_nested_quotes(str_)

        if str_ in self.namespace or not isinstance(cast_str_to_int_float_bool_or_str(str_), str):  # object
            return str_
        else:  # str
            return '\'{}\''.format(str_)
