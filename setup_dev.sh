#!/usr/bin/env bash

# Install notebook extension
pip install -e . --no-deps

# Simpli
jupyter nbextension install --py --sys-prefix simpli --symlink
jupyter nbextension enable --py --sys-prefix simpli
jupyter serverextension enable --py --sys-prefix simpli

# ipywidgets
jupyter nbextension install --py --sys-prefix widgetsnbextension
jupyter nbextension enable --py --sys-prefix widgetsnbextension

# Declarative widgets
jupyter nbextension install --py --sys-prefix declarativewidgets
jupyter nbextension enable --py --sys-prefix declarativewidgets
jupyter serverextension enable --py --sys-prefix declarativewidgets

jupyter notebook ~
