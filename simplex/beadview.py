from ipywidgets import widgets as w
from functools import partial
# from dominate.tags import *


class BeadView:
    '''
    Represents the bead view.
    '''
    INPUT_FLAG = 'input'
    OPT_INPUT_FLAG = 'opt_input'
    OUTPUT_FLAG = 'output'

    def __init__(self, chain, bead, global_n, local_n, cwd):
        self.my_chain = chain
        self.bead = bead
        self.globals = global_n
        self.locals = local_n
        self.cwd = cwd

        self.fields = {self.INPUT_FLAG: {},
                       self.OPT_INPUT_FLAG: {},
                       self.OUTPUT_FLAG: []
                       }

    def panel_heading(self):
        heading = w.Box().add_class('panel-heading')
        text = w.HTML('<h1>' + self.bead.label + '</h1>')
        heading.children = tuple([text])
        return heading

    def panel_body(self):
        # shorter reference
        bead = self.bead

        # submit callback
        run_callback = partial(self.my_chain.submit,
                               self.fields,
                               self.bead)

        # define panel-body
        body = w.Box().add_class('panel-body')

        # create input fields
        input_elements = [w.HTML('<h3>Input Parameters<h3/>')]
        input_elements.extend([self.text_field(arg['label'],
                                               arg['description'],
                                               self.INPUT_FLAG,
                                               arg['arg_name'])
                               for arg in bead.required_args])

        opt_input_elements = [w.HTML('<h3>Optional Input Parameters<h3/>')]
        opt_input_elements.extend([self.text_field(arg['label'],
                                                   arg['description'],
                                                   self.OPT_INPUT_FLAG,
                                                   arg['arg_name'])
                                   for arg in bead.optional_args])

        # create output fields
        output_elements = [w.HTML('<h3>Output Parameters<h3/>')]
        output_elements.extend([self.text_field(arg['label'],
                                                arg['description'],
                                                self.OUTPUT_FLAG)
                                for arg in bead.return_names])

        # define run button
        run_button = w.Button(description="RUN")
        run_button.add_class('btn').add_class('btn-primary').add_class('run-btn')
        run_button.on_click(run_callback)

        # add to body
        all_elements = []
        all_elements.extend(input_elements)
        all_elements.extend(opt_input_elements)
        all_elements.extend(output_elements)
        all_elements.append(run_button)
        body.children = tuple(all_elements)

        return body

    def text_field(self, name, tooltip, flag, arg_name=''):
        '''
        flag - flag for input or output field
        '''
        # submit callback
        run_callback = partial(self.my_chain.submit,
                               self.fields,
                               self.bead)

        # parent wrapper
        parent = w.Box().add_class('my-text-field')
        field = w.Text(description=name).add_class('form-group')
        field.on_submit(run_callback)
        help_button = w.Button(description='?', tooltip=tooltip)

        parent.children = tuple([field, help_button])

        # save field
        if flag == self.OUTPUT_FLAG:
            self.fields[flag].append(field)
        else:
            self.fields[flag][arg_name] = field
        return parent

    def createPanel(self):
        '''
        Creates a form for a given method configuration.

        Returns
        -----
        widgets.VBox
            Contains list of generated widgets.
        '''
        panel = w.Box().add_class('panel').add_class(
            'panel-default').add_class('my-panel')
        panel.children = tuple([self.panel_heading(), self.panel_body()])
        return panel

    def submit(self, button):
        self.my_chain.submit(self.fields, bead)
