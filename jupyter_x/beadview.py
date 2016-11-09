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

        # create input fields
        for arg in bead.requiredArgs:
            w = widgets.Text()
            entry = widgets.VBox(
                [widgets.Label(arg['label']), w])
            entryBoxes.append(entry)
            self.entryWidgets.append(w)

        # create submit button
        submitButton = widgets.Button(description="Run")
        entryBoxes.append(submitButton)

        # register button for submit
        submitCallback = partial(self.myChain.submit,
                                 self.entryWidgets, bead.functionName, bead.libraryName, bead.libraryPath)
        submitButton.on_click(submitCallback)
        for entry in self.entryWidgets:
            entry.on_submit(submitCallback)

        return widgets.VBox(tuple(entryBoxes))

    def submit(self, button):
        self.myChain.submit(entryWidgets, functionName,
                            libraryName, libraryPath)
