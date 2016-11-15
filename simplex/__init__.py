from ipywidgets import widgets
from traitlets import Unicode, Dict
from .chain import Chain


def _jupyter_nbextension_paths():
    return [dict(
        section="notebook",
        # the path is relative to the `my_fancy_module` directory
        src="static",
        # directory in the `nbextension/` namespace
        dest="simplex",
        # _also_ in the `nbextension/` namespace
        require="simplex/main")]


def _jupyter_server_extension_paths():
    return [{
        "module": "simplex"
    }]


def load_jupyter_server_extension(nbapp):
    nbapp.log.info("SimpleX enabled!")
