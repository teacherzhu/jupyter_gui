class Task:
    def __init__(self, task_dict):

        # Usage:
        #   sys.path.insert(0, library_path)
        #   from library_name import function_name
        self.library_path = task_dict['library_path']  # str
        self.library_name = task_dict['library_name']  # str
        self.function_name = task_dict['function_name']  # str
        self.label = task_dict['label']  # str
        self.description = task_dict['description']  # str

        # Required, default, and/or optional arguments
        self.required_args = task_dict['required_args']  # dict
        self.default_args = task_dict['default_args']  # dict
        self.optional_args = task_dict['optional_args']  # dict

        # Return names
        self.return_names = task_dict['returns']  # list
