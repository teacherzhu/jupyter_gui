from IPython import get_ipython  # For syntax (re-imported by default when a Notebook starts)


# ======================================================================================================================
# Define functions
# ======================================================================================================================
def sync_notebook_to_manager():
    """
    Sync namespace: Notebook ==> Manager
    :return:
    """

    mgr.update_namespace(globals())


def sync_manager_to_notebook():
    """
    Sync namespace: Manager ==> Notebook
    :return: None
    """

    for n, v in mgr.namespace.items():
        globals()[n] = v


def load_gui():
    """
    Load GUI components.
    :return: None
    """

    global dwidgets
    import declarativewidgets as dwidgets

    dwidgets.init()

    imports = '''
        <link rel='import' href='urth_components/iron-form/iron-form.html'
              is='urth-core-import' package='PolymerElements/iron-form'>
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
        '''

    get_ipython().run_cell_magic('HTML', '', imports)


# ======================================================================================================================
# Register
# ======================================================================================================================
# TODO: remove the check?
# Register post execute cell callback
if sync_notebook_to_manager not in get_ipython().events.callbacks['post_execute']:
    get_ipython().events.register('post_execute', sync_notebook_to_manager)

# ======================================================================================================================
# Start up Manager
# ======================================================================================================================

# Initialize a Manager.
from simpli import Manager

# TODO: rename to 'manager'
global mgr
mgr = Manager()
# TODO: remove (nothing to sync in the beginning)?
sync_notebook_to_manager()

# ======================================================================================================================
# Start up Notebook Package
# ======================================================================================================================
get_ipython().magic('load_ext autoreload')
get_ipython().magic('autoreload 2')

# ======================================================================================================================
# Load GUI
# ======================================================================================================================
load_gui()

# TODO: remove?
global json
import json
