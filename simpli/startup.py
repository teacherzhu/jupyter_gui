"""
Contains code to be executed in the invisible 1st Notebook cell when a Notebook
loads or refreshes.
"""

import declarativewidgets
from IPython import get_ipython
from simpli.manager import Manager

# ==============================================================================
# Initialize declarativewidgets
# ==============================================================================
declarativewidgets.init()
get_ipython().run_cell_magic('HTML', '', '''
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
<link rel='import' href='urth_components/paper-header-panel/paper-header-panel.html'
      is='urth-core-import' package='PolymerElements/paper-header-panel'>
<link rel='import' href='urth_components/iron-collapse/iron-collapse.html'
      is='urth-core-import' package='PolymerElements/iron-collapse'>
<link rel='import' href='urth_components/paper-collapse-item/paper-collapse-item.html'
      is='urth-core-import' package='Collaborne/paper-collapse-item'>
''')

# ==============================================================================
# Start up Simpli
# ==============================================================================
# Initialize a Manager
manager = Manager()


def import_export_globals():
    """
    Import (Notebook ==> Manager) & export (Manager ==> Notebook) globals.
    :return: None
    """

    globals().update(manager._globals)
    manager.import_globals(globals())


import_export_globals()

# Register post execute cell callback (get_ipython is imported by when a Notebook starts)
get_ipython().events.register('post_execute', import_export_globals)
