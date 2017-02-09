from IPython import get_ipython  # For syntax (reimported when a Notebook starts by default)

global mgr


def init_libs():
    """

    :return:
    """

    global json
    import json

    from simpli import Manager

    # Initialize a Manager
    global mgr
    mgr = Manager()


def load_web_components():
    """

    :return:
    """

    global dwidgets
    import declarativewidgets as dwidgets

    # Initialize declarative widgets
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


def sync_manager_to_notebook():
    """

    :return:
    """

    # Manager ==> Notebook
    for n, v in mgr.namespace.items():
        globals()[n] = v


def sync_notebook_to_manager():
    """

    :return:
    """

    # Notebook ==> Manager
    mgr.update_namespace(globals())


# Register kernel initialization callback
if (init_libs not in get_ipython().events.callbacks['shell_initialized']):
    get_ipython().events.register('shell_initialized', init_libs)

if (load_web_components not in get_ipython().events.callbacks['shell_initialized']):
    get_ipython().events.register('shell_initialized', load_web_components)

# Register post execute cell callback
if sync_notebook_to_manager not in get_ipython().events.callbacks['post_execute']:
    get_ipython().events.register('post_execute', sync_notebook_to_manager)

# Initial namespace sync
init_libs()
load_web_components()
# TODO: remove?
sync_notebook_to_manager()
