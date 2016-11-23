from .taskmanager import TaskManager


# TODO: understand better
def _jupyter_nbextension_paths():
    """
    Required function to add things to the nbextension path.
    :return: list; List of 1 dictionary
    """

    # section: the path is relative to the execute_task/ directory (if viewing from the repository: it's execute_task/execute_task/)
    # dest: Jupyter sets up: server(such as localhost:8888)/nbextensions/dest/
    # src: Jupyter sees this directory (not all files however) when it looks at dest (server/nbextensions/dest/)
    # require: Jupyter loads this file; things in this javascript will be seen in the javascript namespace
    to_return = {'section': 'notebook', 'src': 'static', 'dest': 'execute_task', 'require': 'execute_task/main'}

    return [to_return]


def _jupyter_server_extension_paths():
    """
    Required function to add things to the server extension path.
    :return: list; List of 1 dictionary
    """

    # module:
    to_return = {'module': 'execute_task'}
    return [to_return]


# TODO: understand better
def load_jupyter_server_extension(nbapp):
    """
    Function to be called when extension is loaded.
    :param nbapp: NotebookWebApplication; handle to the Notebook webserver instance
    :return: None
    """

    nbapp.log.info('SimpleX enabled!')
