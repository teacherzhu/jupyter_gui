import os
import sys
from .bead import Bead
from .beadview import BeadView


class Chain:
    '''
    Controller class used to create Bead instances.
    '''

    def __init__(self, methods, global_n, local_n, cwd):
        self.globals = global_n
        self.locals = local_n
        self.cwd = cwd
        self.beads = []

        for method in methods['tasks']:
            bead = self.createBeadModel(method)
            self.beads.append(bead)

    def createBeadModel(self, methodConfig):
        '''
        Binds configuration to bead model and saves reference.
        '''
        return Bead(methodConfig)

    def createBeadView(self, beadModel):
        '''
        Create a BeadView using bead model data.
        '''
        return BeadView(self, beadModel, self.globals, self.locals,
                        self.cwd)

    # TODO: SEE JAVASCRIPT
    # Submit form callback.
    def submit(self, fields, bead, button):
        values = [entry.value for entry in fields]
        print(values)
        print(bead.functionName)
        print(bead.libraryName)
        print(bead.libraryPath)
        print(button)
        # Verify all parameters are present.
        if None in values or '' in values:
            print('Please provide all parameters.')
            return

        sys.path.insert(0, bead.libraryPath)
        exec('from {} import {} as function'.format(
            bead.libraryName, bead.functionName))
        print("Executing ", bead.libraryName,
              ".", bead.functionName, "...")

    def returnData(self, value, dataType):
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
                return os.path.join(self.cwd, val)

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
