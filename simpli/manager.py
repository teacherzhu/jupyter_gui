import sys
from json import loads, dumps
from os import listdir
from os.path import isdir, isfile, join

from IPython.display import clear_output

from . import HOME_DIR, SIMPLI_JSON_DIR
from .support import get_name, merge_dicts, title_str, cast_str_to_int_float_bool_or_str, reset_encoding


class Manager:
    """
    Manager for a Jupyter Notebook.
    """

    def __init__(self):
        """
        Constructor.
        """

        # Manager namespace, which updates after running each cell
        self._manager_namespace = {}

        # Tasks (and their specifications) keyed by the label, which is the UID
        self._tasks = {}

    # manager_namespace
    @property
    def manager_namespace(self):
        return self._manager_namespace

    @manager_namespace.setter
    def manager_namespace(self, namespace):
        self._manager_namespace = namespace

    # tasks
    @property
    def tasks(self, type='dict'):
        if type == 'dict':
            return self._tasks
        elif type == 'str':
            return dumps(self._tasks)

    @tasks.setter
    def tasks(self, tasks):
        self._tasks = tasks

    # Accessor
    def get_task(self, task_label):
        return self.tasks[task_label]

    def update_task(self, task):
        self.tasks.update(task)

    def update_manager_namespace(self, namespace):
        """
        Update Manager's namespace with namespace.
        :param namespace: dict;
        :return: None
        """

        self.manager_namespace = merge_dicts(self.manager_namespace, namespace)

    def execute_task(self, task_json):
        """
        Execute task.
        :param task_json: dict;
        :return: None
        """

        # Clear any existing output
        clear_output()

        # Get args
        required_args = {a['name']: a['value'] for a in task_json['required_args']}
        default_args = {a['name']: a['value'] for a in task_json['default_args']}
        optional_args = {a['name']: a['value'] for a in task_json['optional_args']}

        # Get returns
        returns = [a['value'] for a in task_json['returns']]

        # Verify inputs
        if None in required_args or '' in required_args:
            print('Missing required_args.')
            return
        if None in returns or '' in returns:
            print('Missing returns.')
            return

        # Call function
        returned = self._path_import_and_execute(task_json['library_path'], task_json['library_name'],
                                                 task_json['function_name'],
                                                 required_args, default_args, optional_args,
                                                 returns)

        # Handle returns
        if len(returns) == 1:
            self.manager_namespace[returns[0]] = returned
        elif len(returns) > 1:
            for n, v in zip(returns, returned):
                self.manager_namespace[n] = v
        else:
            # TODO: think about how to better handle no-returns
            pass

    def _path_import_and_execute(self, library_path, library_name, function_name,
                                 required_args, default_args, optional_args,
                                 returns):
        """
        Execute a task.

        :param library_path: str;
        :param library_name: str;
        :param function_name: str;

        :param required_args: dict;
        :param default_args: dict;
        :param optional_args: dict;

        :param returns: list;

        :return: list; raw output of the function
        """

        print('Updating path, importing function, and executing task ...')

        # Prepend library path
        print('\tsys.path.insert(0, \'{}\')'.format(library_path))
        sys.path.insert(0, library_path)

        # Import function
        code = 'from {} import {} as function'.format(library_name, function_name)
        print('\t{}'.format(code))
        exec(code)

        # Process and merge args
        args = self._merge_and_process_args(required_args, default_args, optional_args)

        # Execute
        print('\tExecuting {} with arguments:'.format(locals()['function']))
        for n, v in sorted(args.items()):
            print('\t\t{} = {} ({})'.format(n, get_name(v, self.manager_namespace), type(v)))

        return locals()['function'](**args)

    def _merge_and_process_args(self, required_args, default_args, optional_args):
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

        print('Merging and processing arguments ...')

        repeating_args = set(required_args.keys() & default_args.keys() & optional_args.keys())
        if any(repeating_args):
            raise ValueError('Repeated arguments: {}.'.format(required_args))

        merged_args = merge_dicts(required_args, default_args, optional_args)

        processed_args = {}
        for n, v in merged_args.items():

            if v in self.manager_namespace:  # Process as already defined variable from the Notebook environment
                processed_v = self.manager_namespace[v]

            else:  # Process as float, int, bool, or str
                # First assume a list of str to be passed
                processed_v = [cast_str_to_int_float_bool_or_str(s) for s in v.split(',') if s]

                # If there is only 1 item in the assumed list, use it directly
                if len(processed_v) == 1:
                    processed_v = processed_v[0]

            processed_args[n] = processed_v
            print('\t{}: {} > {} ({})'.format(n, v, get_name(processed_v, self.manager_namespace), type(processed_v)))

        return processed_args

    def load_tasks_from_jsons(self, json_directory_path=SIMPLI_JSON_DIR):
        """

        :param json_directory_path: str; the main directory that contains all library directories
        :param record_filepath: str; .json containing all available tasks' specifications
        :param return_type: type; 'dict' or 'str'
        :return: None
        """

        for f in listdir(json_directory_path):
            fp_json = join(json_directory_path, f)
            try:
                self.tasks.update(self._load_tasks_from_json(fp_json))
            except:
                pass

    def _load_tasks_from_json(self, json_filepath):
        """

        :param json_filepath: str; absolute filepath to library.json
        :return: dict;
        """

        print('Loading tasks from {} ...'.format(json_filepath))

        if not isfile(json_filepath):
            raise FileNotFoundError('The file {} isn\'t found or isn\'t an absolute path.'.format(json_filepath))

        # Open .json
        with open(json_filepath) as f:
            read = f.read()
            library = loads(reset_encoding(read))

        tasks = {}

        # Load library path
        if 'library_path' in library:  # Use specified library path
            library_path = library['library_path']

            # # Make sure the library path ends with '/'
            # if not library_path.endswith('/'):
            #     library_path += '/'
            #     print('\tAppended \'/\' to library_path, which is now: {}.'.format(library_path))

            if not isdir(library_path):  # Use absolute path
                library_path = join(HOME_DIR, library_path)
                print('\tAssuming that library_path is relative to the user-home directory: {}.'.format(library_path))

        else:
            raise ValueError('\'library_path\' isn\'t specified in {}.'.format(json_filepath))

        # Load library tasks
        for t in library['tasks']:

            function_path = t['function_path']
            if '.' in function_path:
                split = function_path.split('.')
                library_name = '.'.join(split[:-1])
                function_name = split[-1]
            else:
                raise ValueError('Function path must be like: \'path.to.file.function_name\'.')

            # Task label is this task's UID; so no duplicates are allowed
            if 'label' in t:
                label = t['label']
            else:
                label = '{} (no label)'.format(function_name)

            if label in tasks:  # Label is duplicated
                print('\'{}\' task label is duplicated.; automatically making a new label ...'.format(label))

                i = 2
                new_label = '{} (v{})'.format(label, i)
                while new_label in tasks:
                    i += 1
                    new_label = '{} (v{})'.format(label, i)
                label = new_label

            tasks[label] = {}
            tasks[label]['library_path'] = library_path
            # Load task library name
            tasks[label]['library_name'] = library_name
            # Load task function name
            tasks[label]['function_name'] = function_name
            if 'description' in t:  # Load task description
                tasks[label]['description'] = t['description']
            else:
                tasks[label]['description'] = 'No description.'
            # Load args
            for arg_type in ['required_args', 'optional_args', 'default_args']:
                if arg_type in t:
                    tasks[label][arg_type] = self._process_args(t[arg_type])
                else:
                    tasks[label][arg_type] = []
            # Load returns
            if 'returns' in t:
                tasks[label]['returns'] = self._process_returns(t['returns'])
            else:
                tasks[label]['returns'] = []

        return tasks

    def _load_tasks_from_cell(self, json_filepath):
        """

        :param json_filepath: str;
        :return: dict;
        """
        return

    def _process_args(self, dicts):
        """

        :param dicts: list; list of dict
        :return: dict;
        """

        processed_dicts = []

        for d in dicts:
            processed_d = {}

            # Load name
            processed_d['name'] = d['name']

            if 'value' in d:  # Load default value
                processed_d['value'] = d['value']
            else:
                processed_d['value'] = ''

            if 'label' in d:  # Load label
                processed_d['label'] = d['label']
            else:  # Set label as the name
                processed_d['label'] = title_str(d['name'])

            if 'description' in d:  # Load description
                processed_d['description'] = d['description']
            else:
                processed_d['description'] = 'No description.'

            processed_dicts.append(processed_d)

        return processed_dicts

    def _process_returns(self, dicts):
        """

        :param dicts: list; list of dict
        :return: dict;
        """

        processed_dicts = []

        for d in dicts:
            processed_d = {}

            # Load label
            processed_d['label'] = d['label']

            if 'description' in d:  # Load description
                processed_d['description'] = d['description']
            else:
                processed_d['description'] = 'No description.'

            processed_dicts.append(processed_d)

        return processed_dicts
