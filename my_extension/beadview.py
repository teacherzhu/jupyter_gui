import ipywidgets as widgets
from functools import partial


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
        self.entryWidgets = []

    def createFormView(self):
        '''
        Creates a form for a given method configuration.

        Returns
        -----
        widgets.VBox
            Contains list of generated widgets.
        '''
        bead = self.bead
        entryBoxes = []  # grouped for layout

        # define layouts
        centerLayout = widgets.Layout(display='flex',
                                      align_items='center',
                                      justify_content='center')

        # create header
        headingText = bead.title
        heading = widgets.HTML('<h1>' + headingText + '</h1>')
        entryBoxes.append(heading)

        # create input fields
        for arg in bead.requiredArgs:
            field = widgets.Text(placeholder=arg['label'])
            entryBoxes.append(field)
            self.entryWidgets.append(field)

        # create submit button
        submitButton = widgets.Button(description="Run")
        entryBoxes.append(submitButton)

        # register button for submit
        submitCallback = partial(self.myChain.submit,
                                 self.entryWidgets, bead)
        submitButton.on_click(submitCallback)
        for entry in self.entryWidgets:
            entry.on_submit(submitCallback)

        container = widgets.VBox(children=entryBoxes, layout=centerLayout)

        return container

    def submit(self, button):
        self.myChain.submit(entryWidgets, bead)
