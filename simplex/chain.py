import os
import sys
from .bead import Bead
from .beadview import BeadView
from .engine import simplex


class Chain:
    '''
    Controller class used to create Bead instances.
    '''

    def __init__(self, config, global_n, local_n, cwd):
        self.globals = global_n
        self.locals = local_n
        self.cwd = cwd
        self.beads = []
        self.output = {}

        version = config['version']
        library_path = config['library_path']
        for task in config['tasks']:
            bead = self.createBeadModel(version, library_path, task)
            self.beads.append(bead)

    def createBeadModel(self, version, library_path, task):
        '''
        Binds configuration to bead model and saves reference.
        '''
        return Bead(version, library_path, task)

    def createBeadView(self, beadModel):
        '''
        Create a BeadView using bead model data.
        '''
        return BeadView(self, beadModel, self.globals, self.locals,
                        self.cwd)

    # Submit form callback.
    def submit(self, fields, bead, button):
        input_fields = fields[BeadView.INPUT_FLAG]
        opt_input_fields = fields[BeadView.OPT_INPUT_FLAG]
        output_fields = fields[BeadView.OUTPUT_FLAG]

        # retrieve user input
        input_values = {arg_name: input_fields[
            arg_name].value for arg_name in input_fields}
        opt_input_values = {arg_name: opt_input_fields[
            arg_name].value for arg_name in opt_input_fields}
        return_names = [entry.value for entry in output_fields]
        print(input_values)
        print(opt_input_values)
        print(return_names)
        print(bead.function_name)
        print(bead.library_name)
        print(bead.library_path)
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
        results = simplex(path_to_include=bead.library_path,
                          library_name=bead.library_name,
                          function_name=bead.function_name,
                          req_args=input_values,
                          opt_args=opt_input_values,
                          return_names=return_names)

        for name, value in zip(return_names, results):
            self.output[name] = value
