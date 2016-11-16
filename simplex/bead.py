class Bead:
    '''
    Uses ipywidgets to create a submission form widget.
    Generates command to be executed by Chain class.
    '''

    def __init__(self, version, library_path, config):
        self.version = version
        self.library_path = library_path
        self.library_name = config['library_name']
        self.label = config['label']
        self.function_name = config['function_name']
        self.optional_args = config['optional_args']
        self.required_args = config['required_args']
        self.return_names = config['return_names']
