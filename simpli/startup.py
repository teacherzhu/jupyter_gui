"""
Contains codes to be executed in the invisible 1st Notebook cell when a Notebook loads or refreshes.
"""

import declarativewidgets
from simpli.manager import Manager

# ======================================================================================================================
# Load GUI
# ======================================================================================================================

declarativewidgets.init()

imports = '''
        <link rel='import' href='urth_components/iron-form/iron-form.html'
              is='urth-core-import' package='PolymerElements/iron-form'>
        <link rel='import' href='urth_components/iron-collapse/iron-collapse.html'
              is='urth-core-import' package='PolymerElements/iron-collapse'>
        <link rel='import' href='urth_components/paper-input/paper-input.html'
              is='urth-core-import' package='PolymerElements/paper-input'>
        <link rel='import' href='urth_components/iron-label/iron-label.html'
              is='urth-core-import' package='PolymerElements/iron-label'>
        <link rel='import' href='urth_components/paper-button/paper-button.html'
              is='urth-core-import' package='PolymerElements/paper-button'>
        <link rel='import' href='urth_components/iron-icon/iron-icon.html'
              is='urth-core-import' package='PolymerElements/iron-icon'>
        <link rel='import' href='urth_components/paper-material/paper-material.html'
              is='urth-core-import' package='PolymerElements/paper-material'>
        <link rel='import' href='urth_components/iron-collapse/iron-collapse.html'
              is='urth-core-import' package='PolymerElements/iron-collapse'>
        '''

get_ipython().run_cell_magic('HTML', '', imports)

# ======================================================================================================================
# Start up Simpli
# ======================================================================================================================
# Initialize a Manager
manager = Manager()


def import_export_globals():
    """
    Import (Notebook ==> Manager) & export (Manager ==> Notebook) globals.
    :return: None
    """

    # TODO: test if the sync syncing occurs as expected
    manager.import_export_globals(globals())


# Sync globals with manager
import_export_globals()

# Register post execute cell callback (get_ipython is imported by when a Notebook starts)
get_ipython().events.register('post_execute', import_export_globals)
