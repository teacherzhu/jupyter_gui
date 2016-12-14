#!/usr/bin/env bash

# Clean dev install
rm -rf *.egg-info*
pip uninstall simplex -y

# Install notebook extension
pip install -e .
jupyter nbextension install --py --sys-prefix simplex
jupyter nbextension enable --py --sys-prefix simplex
jupyter serverextension enable --py --sys-prefix simplex

# Enable ipywidgets
jupyter nbextension enable --py --sys-prefix widgetsnbextension

cd $HOME
jupyter notebook
