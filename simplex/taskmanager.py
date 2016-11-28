import sys

from .task import Task
from .taskview import TaskView


# TODO: use '_' prefix for local variables
class TaskManager:
    """
    Controller class. Manages tasks and their views.
    """

    def __init__(self):
        """
        Constructor.
        """

        # List of tasks
        self.tasks = []

        # Most recent Notebook namespace
        self.simplex_namespace = {}

    def update_simplex_namespace(self, namespace):
        """
        Update the notebook_namespace.
        :param namespace: dict;
        :return: None
        """
        self.simplex_namespace = merge_dicts(self.simplex_namespace,
                                             namespace)

    def create_task_view(self, task_dict):
        """
        Create a Task and display it as a TaskView.
        :param task_dict: dict;
        :return: TaskView;
        """

        task = Task(task_dict)
        self.tasks.append(task)

        return TaskView(self, task)

    def submit(self, fields, task):
        """
        Callback function for when the cell runs. Execute function.
        """

        # Retrieve default arguments to execute_task the function
        default_values = {arg['arg_name']: arg['value']
                          for arg in task.default_args}

        # Retrieve fields
        input_fields = fields['input']
        opt_input_fields = fields['optional_input']
        output_fields = fields['output']

        # Retrieve user inputs in the corresponding fields
        input_values = {input_name: field.value for input_name,
                        field in input_fields.items()}
        opt_input_values = {
            input_name: field.value for input_name, field in opt_input_fields.items()}
        return_names = [field.value for field in output_fields]

        # Verify all input parameters are present.
        if None in input_values or '' in input_values:
            print('Please provide all required inputs.')
            return

        # Verify all output parameters are present.
        if None in return_names or '' in return_names:
            print('Please provide all output variable names.')
            return

        # Call function
        results = self.execute_task(task.library_path, task.library_name, task.function_name,
                                    input_values, default_values, opt_input_values, return_names)

        if len(return_names) == 1:
            self.simplex_namespace[return_names[0]] = results
        elif len(return_names) > 1:
            for name, value in zip(return_names, results):
                self.simplex_namespace[name] = value

    def execute_task(self, library_path, library_name, function_name, req_args, default_args, opt_args, return_names):
        """
        Executes named function from specified python package path.

        Takes in arguments for the named function, automatically detecting and
        casting to the appropriate data type. Returns the results of the function.
        :param library_path: str;
        :param library_name: str;
        :param function_name: str;
        :param req_args: dict;
        :param default_args: dict;
        :param opt_args: dict;
        :param return_names: list;
        :return: list; raw output of the named function.
        """

        # Appenda library path
        sys.path.insert(0, library_path)

        # Import function
        print('From {} importing {} ...'.format(library_name, function_name))
        exec('from {} import {} as function'.format(library_name, function_name))

        # Process args
        args = self.process_args(req_args, default_args, opt_args)

        # Execute
        return locals()['function'](**args)

    def process_args(self, req_args, default_args, opt_args):
        """
        Convert input str arguments to corresponding values:
            If the str is the name of a existing variable in the Notebook namespace, use its corresponding value;
            If the str contains ',', convert it into a list of strs
            Try to cast str in the following order and use the 1st match: int, float, bool, and str;
        :param req_args: dict;
        :param default_args: dict;
        :param opt_args: dict;
        :return: dict;
        """

        args = merge_dicts(req_args, default_args, opt_args)
        processed_args = {}

        for arg_name, v in args.items():

            if v in self.simplex_namespace:  # Process as already defined variable from the Notebook environment
                processed = self.simplex_namespace[v]

            else:  # Process as float, int, bool, or string

                # First assume a list of strings to be passed
                processed = [cast_string_to_int_float_bool_or_str(
                    s) for s in v.split(',') if s]

                # If there is only 1 item in the assumed list, use it directly
                if len(processed) == 1:
                    processed = processed[0]

            processed_args[arg_name] = processed

        return processed_args


# ======================================================================================================================
# Helper functions
# ======================================================================================================================
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
