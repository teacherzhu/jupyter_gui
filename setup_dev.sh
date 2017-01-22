#!/usr/bin/env bash

# Install notebook extension
pip install -e . --no-deps
jupyter nbextension install --py --sys-prefix simplex
jupyter nbextension enable --py --sys-prefix simplex
jupyter serverextension enable --py --sys-prefix simplex

# Enable ipywidgets and declarativewidgets
# jupyter nbextension enable --py --sys-prefix widgetsnbextension
# jupyter nbextension enable --py --sys-prefix declarativewidgets
cd $HOME
jupyter notebook
