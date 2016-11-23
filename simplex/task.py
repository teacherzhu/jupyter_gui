class Task:
    '''
    Model for SimpleX task.
    '''

    def __init__(self, version, library_path, config):
        self.version = version
        self.library_path = library_path
        self.library_name = config['library_name']
        self.label = config['label']
        self.function_name = config['function_name']
        self.default_args = config[
            'default_args'] if 'default_args' in config else {}
        self.required_args = config['required_args']
        self.optional_args = config[
            'optional_args'] if 'optional_args' in config else {}
        self.return_names = config['return_names']
