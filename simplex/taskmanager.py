from .engine import simplex
from .task import Task
from .taskview import TaskView


class TaskManager:
    '''
    Controller class used to manage tasks and their views.
    '''

    def __init__(self, config, global_n, local_n, cwd):
        '''
        Constructor for TaskManager class.

        Arguments
        -----
        '''
        self.global_n = global_n
        self.local_n = local_n
        self.cwd = cwd
        self.tasks = []
        self.output = {}

        version = config['version']
        library_path = config['library_path']
        for task in config['tasks']:
            task = self.create_task(version, library_path, task)
            self.tasks.append(task)

    def create_task(self, version, library_path, task):
        '''
        Binds configuration to Task model and saves reference.
        '''
        return Task(version, library_path, task)

    def create_task_view(self, task):
        '''
        Create a TaskView using Task model data.
        '''
        return TaskView(self, task, self.global_n, self.local_n,
                        self.cwd)

    # Submit form callback.
    def submit(self, fields, task, button):
        '''
        Callback function for when the cell is submitted. Executes function.
        '''
        default_values = {arg['arg_name']: arg[
            'value'] for arg in task.default_args}

        for arg in task.default_args:
            arg_name = arg['arg_name']
            arg_value = arg['value']

        input_fields = fields[TaskView.INPUT_FLAG]
        opt_input_fields = fields[TaskView.OPT_INPUT_FLAG]
        output_fields = fields[TaskView.OUTPUT_FLAG]

        # retrieve user input
        input_values = {arg_name: input_fields[
            arg_name].value for arg_name in input_fields}
        opt_input_values = {arg_name: opt_input_fields[
            arg_name].value for arg_name in opt_input_fields}
        return_names = [entry.value for entry in output_fields]

        # Verify all input parameters are present.
        if None in input_values or '' in input_values:
            print('Please provide all required inputs.')
            return

        if len(opt_input_values) == 0:
            opt_input_values = {}

        # Verify all output parameters are present.
        if None in return_names or '' in return_names:
            print('Please provide all output variable names.')
            return

        # Call function
        results = simplex(global_n=self.global_n,
                          path_to_include=task.library_path,
                          library_name=task.library_name,
                          function_name=task.function_name,
                          default_args=default_values,
                          req_args=input_values,
                          opt_args=opt_input_values,
                          return_names=return_names)

        # TODO: test
        print('RETURN NAMES LENGTH: ', return_names)
        if len(return_names) == 1:
            self.output[return_names[0]] = results
        elif len(return_names) > 1:
            for name, value in zip(return_names, results):
                self.output[name] = value
