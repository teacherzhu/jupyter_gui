#!/usr/bin/env bash

# Install notebook extension
pip install -e . --no-deps
jupyter nbextension install --py --sys-prefix simplex
jupyter nbextension enable --py --sys-prefix simplex
jupyter serverextension enable --py --sys-prefix simplex

# Enable ipywidgets
jupyter nbextension enable --py --sys-prefix widgetsnbextension

cd $HOME
jupyter notebook
