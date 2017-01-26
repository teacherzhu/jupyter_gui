#!/usr/bin/env bash

# Install notebook extension
pip install -e . --no-deps
jupyter nbextension install --py --sys-prefix simpli
jupyter nbextension enable --py --sys-prefix simpli
jupyter serverextension enable --py --sys-prefix simpli

# Enable ipywidgets and declarativewidgets
# jupyter nbextension enable --py --sys-prefix widgetsnbextension
# jupyter nbextension enable --py --sys-prefix declarativewidgets
cd $HOME
jupyter notebook
