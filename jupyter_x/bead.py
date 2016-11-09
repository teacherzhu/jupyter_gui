

class Bead:
    '''
    Uses ipywidgets to create a submission form widget.
    Generates command to be executed by Chain class.
    '''

    def __init__(self, config):
        self.title = config['title']
        self.functionName = config['function_name']
        self.libraryName = config['library_name']
        self.libraryPath = config['library_path']
        self.optionalArgs = config['optional_args']
        self.requiredArgs = config['required_args']
        self.returns = config['returns']
