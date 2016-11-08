import ipywidgets as _widgets
import os as _os


class Engine:
    def __init__(self, global_n, local_n, cwd):
        self.globals = global_n
        self.locals = local_n
        self.cwd = cwd
        self.taskWidgets = []

    def createTaskWidget(self, args,
                             library_path, library_name, function_name):
        task = self.TaskWidget(args, self.globals, self.locals,
                               self.cwd, library_path, library_name,
                               function_name)
        self.taskWidgets.append(task)
        return task

    def execute(self):
        '''
        Execute command with specified arguments.
        '''

    def _returnData(self, value, dataType):
        '''
        Parse value as specified dataType and return associated data in a variable.

        Parameters
        -----
        dataType : string name of type
            Must be one of the following:
            filename - path to file relative to current working directory
                or full path
            variable - name of variable within global/current local
                namespace of function call
            str - string
            int - integer
            float - float

        Returns
        -----
        Associated data in a variable.
        '''
        def parseFile(val):
            '''
            Returns filepath
            '''
            val = str(val)
            if val.startswith('~') or val.startswith('/'):
                return val
            else:
                return _os.path.join(self.cwd, val)

        def parseVariable(val):
            val = str(val)
            try:
                return locals[val]
            except KeyError:
                try:
                    return globals[val]
                except KeyError:
                    return 'Variable not found'

        def parseString(val):
            return str(val)

        def parseInt(val):
            return int(val)

        def parseFloat(val):
            return float(val)

        switch = {
            'file': parseFile,
            'variable': parseVariable,
            'str': parseString,
            'int': parseInt,
            'float': parseFloat
        }

        try:
            return switch.get(dataType)(value)
        except ValueError:
            print('ValueError')

    class TaskWidget:
        '''
        Uses ipywidgets to create a submission form widget.
        Generates command to be executed by Engine class.
        '''

        def __init__(self, args, global_n, local_n, cwd,
                     library_path, library_name, function_name):
            self.args = args

        def entryForm(self):
            '''
            Creates a specified panel of ipywidgets.

            Parameters
            -----
            args : list of dictionaries
                List of elements with name = label,
                and elements data type and description.
            Returns
            -----
            _widgets.VBox
                Contains list of generated _widgets.
            '''
            # grouped for layout
            entryBoxes = []

            # references to widgets that take input
            entryWidgets = []

            # Submit form callback.
            def submit(b):
                params = [w.value for w in entryWidgets]

                # Verify all parameters are present.
                if None in params or '' in params:
                    print(params)
                    print('Please provide all parameters.')
                else:
                    print(params)
                    exec('from {} import {} as function'.format(
                        self.library_name, self.function_name))

            # generate input
            for arg in self.args:
                w = _widgets.Text()
                w.on_submit(submit)  # register enter key for submit

                dataTypes = arg['data_type']
                typeButtons = _widgets.Dropdown(
                    options=dataTypes,
                    value=dataTypes[0],
                    description='Data type:',
                    button_style='')

                entry = _widgets.VBox(
                    [_widgets.Label(arg['label']), w, typeButtons])
                entryBoxes.append(entry)
                entryWidgets.append(w)

            content = tuple(entryBoxes)
            container = _widgets.VBox(content)

            submitButton = _widgets.Button(description="Submit")
            submitButton.on_click(submit)  # register button for submit

            return _widgets.VBox(tuple([container, submitButton]))
