class Task:
    def __init__(self, task_dict):

        # Usage:
        #   sys.path.insert(0, library_path)
        #   from library_name import function_name
        self.library_path = task_dict['library_path']  # str
        self.library_name = task_dict['library_name']  # str
        self.function_name = task_dict['function_name']  # str

        # Alias for the task name shown in a widget
        if 'label' in task_dict:
            self.label = task_dict['label']  # str
        else:
            self.label = self.function_name  # str

        # Arguments
        self.required_args = task_dict['required_args']  # dict
        self.default_args = task_dict['default_args'] if 'default_args' in task_dict else {}  # dict
        self.optional_args = task_dict['optional_args'] if 'optional_args' in task_dict else {}  # dict

        # Names to store the returned variables
        self.return_names = task_dict['return_names']  # list
