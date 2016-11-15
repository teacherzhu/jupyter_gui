from ipywidgets import widgets as w
from functools import partial
# from dominate.tags import *
from IPython.core.display import HTML


class BeadView:
    '''
    Represents the bead view.
    '''

    def __init__(self, chain, bead, global_n, local_n, cwd):
        self.myChain = chain
        self.bead = bead
        self.globals = global_n
        self.locals = local_n
        self.cwd = cwd
        self.fields = []

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
        submitCallback = partial(self.myChain.submit,
                                 self.fields, self.bead)

        # define panel-body
        body = w.Box().add_class('panel-body')

        # create input fields
        inputFields = [w.HTML('<h3>Input Parameters<h3/>')]
        inputFields.extend([self.text_field(arg['label'], arg['description'])
                            for arg in bead.requiredArgs])

        # create output fields
        outputFields = [w.HTML('<h3>Output Parameters<h3/>')]
        outputFields.extend([self.text_field(
            arg['label'], arg['description']) for arg in bead.returns])

        # define run button
        runButton = w.Button(description="RUN")
        runButton.add_class('btn').add_class('btn-primary')
        runButton.on_click(submitCallback)

        # add to body
        allElements = []
        allElements.extend(inputFields)
        allElements.extend(outputFields)
        allElements.append(runButton)
        body.children = tuple(allElements)

        return body

    def text_field(self, name, tooltip):
        # submit callback
        submitCallback = partial(self.myChain.submit,
                                 self.fields, self.bead)

        # parent wrapper
        parent = w.Box().add_class('my-text-field')
        field = w.Text(description=name).add_class('form-group')
        helpButton = w.Button(description='?', tooltip=tooltip)

        field.on_submit(submitCallback)

        parent.children = tuple([field, helpButton])
        self.fields.append(field)
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
        self.myChain.submit(self.fields, bead)
