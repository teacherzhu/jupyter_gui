from ipywidgets import widgets as w
from functools import partial
# from dominate.tags import *


class BeadView:
    '''
    Represents the bead view.
    '''

    def __init__(self, chain, bead, global_n, local_n, cwd):
        self.my_chain = chain
        self.bead = bead
        self.globals = global_n
        self.locals = local_n
        self.cwd = cwd
        self.input_fields = []
        self.output_fields = []

    # MDL Themed Components

    def panel_heading(self):
        heading = w.Box().add_class('panel-heading')
        text = w.HTML('<h1>' + self.bead.title + '</h1>')
        heading.children = tuple([text])
        return heading

    def panel_body(self):
        # shorter reference
        bead = self.bead

        # submit callback
        submitCallback = partial(self.my_chain.submit,
                                 self.input_fields,
                                 self.output_fields,
                                 self.bead)

        # define panel-body
        body = w.Box().add_class('panel-body')

        # create input fields
        input_elements = [w.HTML('<h3>Input Parameters<h3/>')]
        input_elements.extend([self.text_field(arg['label'],
                                               arg['description'],
                                               True, arg['arg_name'])
                               for arg in bead.requiredArgs])

        # create output fields
        output_elements = [w.HTML('<h3>Output Parameters<h3/>')]
        output_elements.extend([self.text_field(arg['label'],
                                                arg['description'], False)
                                for arg in bead.returns])

        # define run button
        run_button = w.Button(description="RUN")
        run_button.add_class('btn').add_class('btn-primary')
        run_button.on_click(submitCallback)

        # add to body
        all_elements = []
        all_elements.extend(input_elements)
        all_elements.extend(output_elements)
        all_elements.append(run_button)
        body.children = tuple(all_elements)

        return body

    def text_field(self, name, tooltip, is_in_else_out, arg_name=''):
        '''
        is_in_else_out - flag for input or output field
        '''
        # submit callback
        submitCallback = partial(self.my_chain.submit,
                                 self.input_fields,
                                 self.output_fields,
                                 self.bead)

        # parent wrapper
        parent = w.Box().add_class('my-text-field')
        field = w.Text(description=name).add_class('form-group')
        field.on_submit(submitCallback)
        helpButton = w.Button(description='?', tooltip=tooltip)

        parent.children = tuple([field, helpButton])

        # append to input/output list correclty
        if is_in_else_out:
            self.input_fields[arg_name] = field
        else:
            self.output_fields.append(field)
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
        self.my_chain.submit(self.input_fields, self.output_fields, bead)
