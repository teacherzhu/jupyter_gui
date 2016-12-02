import sys
from IPython.display import clear_output

from .support import merge_dicts, cast_string_to_int_float_bool_or_str, get_name
from .task import Task
from .taskview import TaskView


# TODO: use '_' prefix for local variables
class TaskManager:
    """
    Controller class that manages tasks and their views.
    """

    def __init__(self):
        """
        Constructor.
        """

        # List of tasks
        self.tasks = []

        # Most recent Jupyter Notebook namespace
        self.simplex_namespace = {}

    def update_simplex_namespace(self, namespace):
        """
        Update with the notebook_namespace.
        :param namespace: dict;
        :return: None
        """

        self.simplex_namespace = merge_dicts(self.simplex_namespace, namespace)

    def create_task_view(self, task_dict):
        """
        Make a Task and display it as a TaskView.
        :param task_dict: dict;
        :return: TaskView;
        """

        # Make a new Task
        task = Task(task_dict)
        self.tasks.append(task)

        # Return its TaskView
        return TaskView(self, task)

    def submit(self, fields, task):
        """
        Execute function for when the cell runs.
        """

        # Retrieve default arguments
        default_args = {arg['arg_name']: arg['value'] for arg in task.default_args}

        # Retrieve required and/or optional arguments
        # TODO: rename the keys
        required_args = {input_name: field.value for input_name, field in fields['required_args'].items()}
        optional_args = {input_name: field.value for input_name, field in fields['optional_args'].items()}
        returns = [field.value for field in fields['returns']]

        # Verify all input parameters are present.
        if None in required_args or '' in required_args:
            print('Please provide all required arguments.')
            return

        # Verify all output parameters are present.
        if None in returns or '' in returns:
            print('Please provide all return names.')
            return

        # Clear any existing output
        clear_output()

        # Call function
        returned = self.execute_task(task.library_path, task.library_name, task.function_name,
                                     required_args, default_args, optional_args, returns)

        if len(returns) == 1:
            self.simplex_namespace[returns[0]] = returned
        elif len(returns) > 1:
            for name, value in zip(returns, returned):
                self.simplex_namespace[name] = value

    def execute_task(self, library_path, library_name, function_name, required_args, default_args, optional_args,
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

        print('Executing ...')

        # Append a library path
        # TODO: what's the effect of the last '/' in the path?
        print('\tsys.path.insert(0, \'{}\')'.format(library_path))
        sys.path.insert(0, library_path)

        # Import function
        print('\tfrom {} import {} as function'.format(library_name, function_name))
        exec('from {} import {} as function'.format(library_name, function_name))

        # Process args
        args = self.process_args(required_args, default_args, optional_args)

        # Execute
        print('\n\tExecuting {}:'.format(locals()['function']))
        for a, v in sorted(args.items()):
            print('\t\t{} = {} ({})'.format(a, get_name(v, self.simplex_namespace), type(v)))

        return locals()['function'](**args)

    def process_args(self, required_args, default_args, optional_args):
        """
        Convert input str arguments to corresponding values:
            If the str is the name of a existing variable in the Notebook namespace, use its corresponding value;
            If the str contains ',', convert it into a list of str
            Try to cast str in the following order and use the 1st match: int, float, bool, and str;
        :param required_args: dict;
        :param default_args: dict;
        :param optional_args: dict;
        :return: dict; merged dict
        """

        # print('Processing arguments ...')

        if any(set(required_args.keys() & default_args.keys() & optional_args.keys())):
            raise ValueError('Argument {} is duplicated.')

        args = merge_dicts(required_args, default_args, optional_args)
        processed_args = {}

        for n, v in args.items():

            if v in self.simplex_namespace:  # Process as already defined variable from the Notebook environment
                processed_v = self.simplex_namespace[v]

            else:  # Process as float, int, bool, or string
                # First assume a list of strings to be passed
                processed_v = [cast_string_to_int_float_bool_or_str(s) for s in v.split(',') if s]

                # If there is only 1 item in the assumed list, use it directly
                if len(processed_v) == 1:
                    processed_v = processed_v[0]

            processed_args[n] = processed_v
            # print('\t{}: {} ==> {} ({})'.format(n, v, get_name(processed_v, self.simplex_namespace), type(processed_v)))

        return processed_args
